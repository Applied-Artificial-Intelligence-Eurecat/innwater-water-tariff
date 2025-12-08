import asyncio
from datetime import timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from src.core.auth import authenticate_user, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, \
    get_current_active_user
from src.core.database import get_db
from src.core.models import User, Simulation, Project, StatusEnum, DemandConfiguration, IBTEauPotable, BlockEauPotable, \
    IBTSanitation, BlockSanitation
from src.initial.graphics_service import generate_par_affordability_plot, generate_consumption_plot, \
    generate_tbse_pens_parade_consumptions_plot, generate_tbse_consumption_deviation_losses_cost_recovery_plot, \
    generate_ibt_pens_parade_consumptions_plot
from src.initial.initial_service import create_ibt_parameters, create_demand, create_population, create_primitives
from src.initial.population_service import generate_and_create_population_plot, PopulationPlotModel, \
    save_population_data_given_simulation_info
from src.initial.processing_service import start_processing_and_calculating_simulation
from src.initial.schemas import SimulationPayload, DuplicationSchema, GetSimulationPayload, LaunchModel, PopulationModel
from src.initial.schemas import UserCreate, Token, DemandModel, CoefficientModel, \
    WaterServiceCostModel, PrimitivesModel, EnvironmentalModel, TaxSectionModel, TaxModel, SocialDataModel, TariffModel, \
    TariffSectionModel, ConsumptionThresholds
from src.small_assessment.new_calculator_service import get_or_create_simulation_from_payload

initial_router = APIRouter(
    prefix="/initial",
    tags=["initial"],
    responses={404: {"description": "Not found"}},
)


@initial_router.post("/population/plot")
async def get_population_plot(input: PopulationPlotModel) -> StreamingResponse:
    """
    Endpoint to generate a scatter plot chart to validate the population.

    Args:
        input_data: The population model containing bd, eps, and std parameters

    Returns:
        dict: Contains the base64 encoded PNG image and content type
    """
    buf = generate_and_create_population_plot(input.total_subscribers, input.sanitation_subscribers, input.bd,
                                              input.eps,
                                              input.std, input.random_seed)
    return StreamingResponse(buf, media_type="image/png")


@initial_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login, get an access token for future requests.

    Args:
        form_data: OAuth2 form containing username (email) and password
        db: Database session

    Returns:
        Token: Contains access token and token type
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@initial_router.post("/user", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user_data: The user data containing email and password
        db: Database session

    Returns:
        dict: Contains the created user information (without password)
    """
    # Check if user with this email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user with hashed password
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password=hashed_password
    )

    # Add to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return user info (without password)
    return {"id": new_user.id, "email": new_user.email, "message": "User created successfully"}


@initial_router.get("/users/me", response_model=Dict[str, Any])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        dict: Contains the current user information (without password)
    """
    return {"id": current_user.id, "email": current_user.email}


@initial_router.post("/simulation/new")
async def create_and_save_simulation(
        payload: SimulationPayload,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    # Use the authenticated user from the JWT token
    project = db.query(Project).filter(Project.user_id == current_user.id).first()
    if project is None:
        project = Project(name="Default Project", user_id=current_user.id)
        db.add(project)
        db.commit()
    simulation = Simulation(
        name=payload.launch.simulation_name,
        number_of_periods=payload.launch.periods,
        status=StatusEnum.created,
        project_id=project.project_id
    )
    db.add(simulation)
    db.commit()
    await create_primitives(db, payload, simulation)
    await create_population(db, payload, simulation)
    await create_demand(db, payload, simulation)
    await create_ibt_parameters(db, payload, simulation)
    db.commit()

    df = await save_population_data_given_simulation_info(
        total_subscribers=simulation.primitives.cost_potable_water.subscribers_number,
        sanitation_subscribers=simulation.primitives.cost_sanitation.subscribers_number,
        bd=simulation.population.database_path,
        eps=simulation.population.eps,
        std=simulation.population.std,
        use_original_datasource=simulation.population.original_datasource,
        simulation_id=simulation.id,
    )

    asyncio.create_task(start_processing_and_calculating_simulation(simulation.id, payload, df, db),
                        name=f"start processing {simulation.id}")

    return {
        "status": "success",
        "message": "Simulation created successfully",
        "data": {
            "simulation_id": simulation.id,
            "name": simulation.name,
            "status": simulation.status.value,
            "project_id": project.project_id
        }
    }


@initial_router.post("/simulation/{simulation_id}/duplicate")
async def duplicate_simulation(simulation_id: int, duplication_payload: DuplicationSchema,
                               current_user: User = Depends(get_current_active_user),
                               db: Session = Depends(get_db)):
    simulation: Dict = await get_simulation(simulation_id, current_user, db)
    payload: GetSimulationPayload = simulation['data']
    payload.launch.simulation_name = duplication_payload.new_name
    simulation_payload = SimulationPayload(
        primitives=payload.primitives,
        population=payload.population,
        tarification=payload.tariff,
        demande=payload.demand,
        launch=payload.launch
    )
    return await create_and_save_simulation(simulation_payload, current_user, db)


@initial_router.get("/simulations", response_model=Dict[str, Any])
async def list_user_simulations(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Get all simulations for the current authenticated user.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        dict: Contains a list of simulations with their details
    """
    # Query all simulations associated with the user's projects
    simulations = db.query(Simulation).join(Project).filter(Project.user_id == current_user.id).all()

    # Format the response
    simulation_list = []
    for sim in simulations:
        simulation_list.append({
            "id": sim.id,
            "name": sim.name,
            "status": sim.status.value,
            "number_of_periods": sim.number_of_periods,
            "project_id": sim.project_id
        })

    return {
        "status": "success",
        "message": f"Found {len(simulation_list)} simulations",
        "data": simulation_list
    }


@initial_router.put("/simulation/{simulation_id}/edit")
async def edit_simulation(simulation_id: int, payload: SimulationPayload,
                          current_user: User = Depends(get_current_active_user),
                          db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Update basic simulation properties
    simulation.name = payload.launch.simulation_name
    simulation.number_of_periods = payload.launch.periods
    db.add(simulation)

    # Update population
    if simulation.population:
        simulation.population.eps = payload.population.eps
        simulation.population.std = payload.population.std
        simulation.population.database_path = payload.population.bd
        db.add(simulation.population)
    else:
        await create_population(db, payload, simulation)

    # Update demand configuration
    demand_config = db.query(DemandConfiguration).filter(DemandConfiguration.simulation_id == simulation.id).first()
    if demand_config:
        demand_config.a = payload.demand.coefficients.a0
        demand_config.b = payload.demand.coefficients.a1
        demand_config.c = payload.demand.coefficients.a2
        demand_config.d = payload.demand.coefficients.a3
        demand_config.e = payload.demand.coefficients.a4
        demand_config.f = payload.demand.coefficients.a5
        demand_config.g = payload.demand.coefficients.a6
        demand_config.perception_parameter = payload.demand.k
        demand_config.pool = payload.demand.has_pool
        demand_config.garden = payload.demand.has_garden
        db.add(demand_config)
    else:
        await create_demand(db, payload, simulation)

    # Update IBT parameters for potable water
    ibt_potable = db.query(IBTEauPotable).filter(IBTEauPotable.simulation_id == simulation.id).first()
    if ibt_potable:
        ibt_potable.abonnement = payload.tariff.drinking_water.subscription
        db.add(ibt_potable)

        # Delete existing blocks and create new ones
        db.query(BlockEauPotable).filter(BlockEauPotable.ibt_id == ibt_potable.id).delete()
        for potable_water_block in payload.tariff.drinking_water.usage_tiers:
            db.add(BlockEauPotable(
                seuil=potable_water_block.threshold,
                price=potable_water_block.price,
                ibt_id=ibt_potable.id,
            ))
    else:
        # Create new IBT parameters if they don't exist
        ibt_potable = IBTEauPotable(
            abonnement=payload.tariff.drinking_water.subscription,
            simulation_id=simulation.id
        )
        db.add(ibt_potable)
        db.commit()
        for potable_water_block in payload.tariff.drinking_water.usage_tiers:
            db.add(BlockEauPotable(
                seuil=potable_water_block.threshold,
                price=potable_water_block.price,
                ibt_id=ibt_potable.id,
            ))

    # Update IBT parameters for sanitation
    ibt_sanitation = db.query(IBTSanitation).filter(IBTSanitation.simulation_id == simulation.id).first()
    if ibt_sanitation:
        ibt_sanitation.abonnement = payload.tariff.sanitation.subscription
        db.add(ibt_sanitation)

        # Delete existing blocks and create new ones
        db.query(BlockSanitation).filter(BlockSanitation.ibt_id == ibt_sanitation.id).delete()
        for sanitation_block in payload.tariff.sanitation.usage_tiers:
            db.add(BlockSanitation(
                seuil=sanitation_block.threshold,
                price=sanitation_block.price,
                ibt_id=ibt_sanitation.id,
            ))
    else:
        # Create new IBT parameters if they don't exist
        ibt_sanitation = IBTSanitation(
            abonnement=payload.tariff.sanitation.subscription,
            simulation_id=simulation.id
        )
        db.add(ibt_sanitation)
        db.commit()
        for sanitation_block in payload.tariff.sanitation.usage_tiers:
            db.add(BlockSanitation(
                seuil=sanitation_block.threshold,
                price=sanitation_block.price,
                ibt_id=ibt_sanitation.id,
            ))

    # Update primitives
    if simulation.primitives:
        # Update potable water costs
        if simulation.primitives.cost_potable_water:
            simulation.primitives.cost_potable_water.fixed_costs = payload.primitives.drinking_water.fixed_costs
            simulation.primitives.cost_potable_water.variable_costs = payload.primitives.drinking_water.variable_costs
            simulation.primitives.cost_potable_water.subscribers_number = payload.primitives.drinking_water.number_of_subscribers
            db.add(simulation.primitives.cost_potable_water)

        # Update sanitation costs
        if simulation.primitives.cost_sanitation:
            simulation.primitives.cost_sanitation.fixed_costs = payload.primitives.sanitation.fixed_costs
            simulation.primitives.cost_sanitation.variable_costs = payload.primitives.sanitation.variable_costs
            simulation.primitives.cost_sanitation.subscribers_number = payload.primitives.sanitation.number_of_subscribers
            db.add(simulation.primitives.cost_sanitation)

        # Update environmental costs
        if simulation.primitives.environmental_costs:
            simulation.primitives.environmental_costs.fixed_costs = payload.primitives.environment.fixed_costs_per_year
            simulation.primitives.environmental_costs.variable_costs = payload.primitives.environment.average_variable_cost
            db.add(simulation.primitives.environmental_costs)

        # Update tax costs
        if simulation.primitives.tax_costs:
            simulation.primitives.tax_costs.vat_drinking_water = payload.primitives.taxation.drinking_water.vat
            simulation.primitives.tax_costs.fee_drinking_water = payload.primitives.taxation.drinking_water.fees
            simulation.primitives.tax_costs.vat_sanitation = payload.primitives.taxation.sanitation.vat
            simulation.primitives.tax_costs.fee_sanitation = payload.primitives.taxation.sanitation.fees
            db.add(simulation.primitives.tax_costs)

        # Update social costs
        if simulation.primitives.social_costs:
            simulation.primitives.social_costs.car_threshold = payload.primitives.social_data.threshold_car
            simulation.primitives.social_costs.par_threshold = payload.primitives.social_data.threshold_par
            simulation.primitives.social_costs.poverty_threshold = payload.primitives.social_data.poverty
            db.add(simulation.primitives.social_costs)
    else:
        await create_primitives(db, payload, simulation)

    db.commit()

    df = await save_population_data_given_simulation_info(
        total_subscribers=simulation.primitives.cost_potable_water.subscribers_number,
        sanitation_subscribers=simulation.primitives.cost_sanitation.subscribers_number,
        bd=simulation.population.database_path,
        eps=simulation.population.eps,
        std=simulation.population.std,
        use_original_datasource=simulation.population.original_datasource,
        simulation_id=simulation.id,
    )

    asyncio.create_task(start_processing_and_calculating_simulation(simulation.id, payload, df, db),
                        name=f"start processing {simulation.id}")

    return {
        "status": "success",
        "message": "Simulation updated successfully",
        "data": {
            "simulation_id": simulation.id,
            "name": simulation.name,
            "status": simulation.status.value,
        }
    }


@initial_router.get("/simulation/{simulation_id}", response_model=dict)
async def get_simulation(simulation_id: int, current_user: User = Depends(get_current_active_user),
                         db: Session = Depends(get_db)):
    """
    Get details of a specific simulation.
    """
    get_simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    return {
        "status": "success",
        "message": f"Found simulation {simulation_id}",
        "data": get_simulation_payload
    }


async def get_simulation_payload_from_db(current_user, db, simulation_id, get_simulation_db=False):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    # Get Demand
    demand_config: DemandConfiguration | None = db.query(DemandConfiguration).filter(
        DemandConfiguration.simulation_id == simulation.id).first()
    if demand_config is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    get_simulation_payload = GetSimulationPayload(id=simulation.id, demande=DemandModel(
        coefficients=CoefficientModel(a0=demand_config.a, a1=demand_config.b, a2=demand_config.c, a3=demand_config.d,
                                      a4=demand_config.e, a5=demand_config.f, a6=demand_config.g, ),
        k=demand_config.perception_parameter, has_garden=demand_config.garden, has_pool=demand_config.pool, ),
                                                  launch=LaunchModel(simulation_name=simulation.name,
                                                                     periods=simulation.number_of_periods, ),
                                                  population=PopulationModel(bd=simulation.population.database_path,
                                                                             eps=simulation.population.eps,
                                                                             std=simulation.population.std,
                                                                             original_datasource=simulation.population.original_datasource,),
                                                  primitives=PrimitivesModel(ep=WaterServiceCostModel(
                                                      couts_fixes=simulation.primitives.cost_potable_water.fixed_costs,
                                                      couts_variables=simulation.primitives.cost_potable_water.variable_costs,
                                                      number_of_subscribers=simulation.primitives.cost_potable_water.subscribers_number),
                                                      assainissement=WaterServiceCostModel(
                                                          couts_fixes=simulation.primitives.cost_sanitation.fixed_costs,
                                                          couts_variables=simulation.primitives.cost_sanitation.variable_costs,
                                                          number_of_subscribers=simulation.primitives.cost_sanitation.subscribers_number),
                                                      environnement=EnvironmentalModel(
                                                          couts_fixes_par_an=simulation.primitives.environmental_costs.fixed_costs,
                                                          couts_variable_moyen=simulation.primitives.environmental_costs.variable_costs, ),
                                                      taxation=TaxSectionModel(drinking_water=TaxModel(
                                                          vat=simulation.primitives.tax_costs.vat_drinking_water,
                                                          fees=simulation.primitives.tax_costs.fee_drinking_water, ),
                                                          sanitation=TaxModel(
                                                              vat=simulation.primitives.tax_costs.vat_sanitation,
                                                              fees=simulation.primitives.tax_costs.fee_sanitation, )),
                                                      social_data=SocialDataModel(
                                                          threshold_par=simulation.primitives.social_costs.car_threshold,
                                                          threshold_car=simulation.primitives.social_costs.par_threshold,
                                                          poverty=simulation.primitives.social_costs.poverty_threshold)),
                                                  status=simulation.status.value,
                                                  tarification=await create_tariff_model_payload_from_simulation(
                                                      simulation))
    if get_simulation_db:
        return get_simulation_payload, simulation
    return get_simulation_payload


async def create_tariff_model_payload_from_simulation(simulation):
    return TariffModel(
        ep=TariffSectionModel(
            abonnement=simulation.ibt_eau_potable.abonnement,
            usage_tiers=[
                ConsumptionThresholds(
                    seuil=b.seuil,
                    prix=b.price,
                )
                for b in
                simulation.ibt_eau_potable.blocks
            ]
        ),
        assainissement=TariffSectionModel(
            abonnement=simulation.ibt_sanitation.abonnement,
            usage_tiers=[
                ConsumptionThresholds(
                    seuil=b.seuil,
                    prix=b.price,
                )
                for b in
                simulation.ibt_sanitation.blocks
            ]

        )
    )


@initial_router.get("/simulation/{simulation_id}/population_plot")
async def get_population_plot_given_simulation(simulation_id: int,
                                               current_user: User = Depends(get_current_active_user),
                                               db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    buf = generate_and_create_population_plot(
        total_subscribers=simulation.primitives.cost_potable_water.subscribers_number,
        sanitation_subscribers=simulation.primitives.cost_sanitation.subscribers_number,
        bd=simulation.population.database_path,
        eps=simulation.population.eps,
        std=simulation.population.std,
        random_seed=42,
    )
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/tbse_par_plot")
async def get_tbse_par_plot(simulation_id: int, current_user: User = Depends(get_current_active_user),
                            db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    print(simulation.id, simulation_payload)
    simulation_finished = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    buf = generate_par_affordability_plot(simulation_payload, simulation_finished.level_oecd,
                                          simulation_finished.par_tbse, 'TBSE')
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/ibt_par_plot")
async def get_ibt_par_plot(simulation_id: int, current_user: User = Depends(get_current_active_user),
                           db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    simulation_finished = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    buf = generate_par_affordability_plot(simulation_payload, simulation_finished.level_oecd,
                                          simulation_finished.par_ibt, 'IBT')
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/tbse_consumption_plot")
async def get_tbse_consumption_plot(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                    db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    simulation_finished = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    buf = generate_consumption_plot(simulation_finished.level_oecd, simulation_finished.tbse_consumption, feat='TBSE')
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/ibt_consumption_plot")
async def get_ibt_consumption_plot(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                   db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    simulation_finished = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    buf = generate_consumption_plot(simulation_finished.level_oecd,
                                    simulation_finished.bcp_consumptions[simulation_finished.simulation.launch.periods],
                                    feat='IBT')
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/tbse_pens_parade_consumption_plot")
async def get_pens_parade_consumption_plot(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                           db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    calculator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)
    buf = generate_tbse_pens_parade_consumptions_plot(calculator)
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/ibt_pens_parade_consumption_plot")
async def get_pens_parade_consumption_plot(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                           db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)

    calculator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    buf = generate_ibt_pens_parade_consumptions_plot(calculator)
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/tbse_consumption_deviation_loses_cost_recovery_plot")
async def get_consumption_deviation_loses_cost_recovery_plot(simulation_id: int,
                                                             current_user: User = Depends(get_current_active_user),
                                                             db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    calculator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    buf = generate_tbse_consumption_deviation_losses_cost_recovery_plot(calculator,
                                                                        calculator.tbse_consumption_per_trim, 'TBSE')
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/ibt_consumption_deviation_loses_cost_recovery_plot")
async def get_consumption_deviation_loses_cost_recovery_plot(simulation_id: int,
                                                             current_user: User = Depends(get_current_active_user),
                                                             db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    calculator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    buf = generate_tbse_consumption_deviation_losses_cost_recovery_plot(calculator, calculator.bcp_consumptions[
        calculator.simulation.launch.periods], 'IBT')
    return StreamingResponse(buf, media_type="image/png")


@initial_router.delete("/simulation/{simulation_id}")
async def delete_simulation(simulation_id: int, current_user: User = Depends(get_current_active_user),
                            db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    db.delete(simulation)
    db.commit()
    return {
        "status": "success",
        "message": f"Simulation {simulation_id} deleted successfully",
    }
