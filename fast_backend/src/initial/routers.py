from datetime import timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from src.core.auth import authenticate_user, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, \
    get_current_active_user
from src.core.database import get_db
from src.core.models import User, Simulation, Project, StatusEnum, DemandConfiguration
from src.initial.graphics_service import generate_tbse_par_affordability_plot, generate_tbse_consumption_plot, \
    generate_pens_parade_consumptions_plot, generate_consumption_deviation_losses_cost_recovery_plot
from src.initial.initial_service import create_ibt_parameters, create_demand, create_population, create_primitives
from src.initial.population_service import generate_population_plot
from src.initial.schemas import PopulationModel, UserCreate, Token, DemandModel, CoefficientModel, \
    WaterServiceCostModel, PrimitivesModel, EnvironmentalModel, TaxSectionModel, TaxModel, SocialDataModel, TariffModel, \
    TariffSectionModel, ConsumptionThresholds
from src.initial.schemas import SimulationPayload

initial_router = APIRouter(
    prefix="/initial",
    tags=["initial"],
    responses={404: {"description": "Not found"}},
)


@initial_router.post("/population/plot")
async def get_population_plot(input: PopulationModel) -> StreamingResponse:
    """
    Endpoint to generate a scatter plot chart to validate the population.

    Args:
        input_data: The population model containing bd, eps, and std parameters

    Returns:
        dict: Contains the base64 encoded PNG image and content type
    """
    buf = await generate_population_plot(input)
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
        status=StatusEnum.initialized,
        project_id=project.project_id
    )
    db.add(simulation)
    db.commit()
    await create_primitives(db, payload, simulation)
    await create_population(db, payload, simulation)
    await create_demand(db, payload, simulation)
    await create_ibt_parameters(db, payload, simulation)
    db.commit()
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


@initial_router.get("/simulation/{simulation_id}")
async def get_simulation(simulation_id: int, current_user: User = Depends(get_current_active_user),
                         db: Session = Depends(get_db)):
    """
    Get details of a specific simulation.
    """
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    # Get Demand
    demand_config: DemandConfiguration | None = db.query(DemandConfiguration).filter(
        DemandConfiguration.simulation_id == simulation.id).first()
    if demand_config is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    return {
        "status": "success",
        "message": f"Found simulation {simulation.id}",
        "data": {
            "id": simulation.id,
            "demand": DemandModel(
                coefficients=CoefficientModel(a0=demand_config.a,
                                              a1=demand_config.b,
                                              a2=demand_config.c,
                                              a3=demand_config.d,
                                              a4=demand_config.e,
                                              a5=demand_config.f,
                                              a6=demand_config.g, ),
                k=demand_config.perception_parameter,
                has_garden=demand_config.garden,
                has_pool=demand_config.pool,
            ),
            "launch": {
                "periods": simulation.number_of_periods,
                "simulation_name": simulation.name,
            },
            "population": {
                "bd": simulation.population.root_database,
                "eps": simulation.population.eps,
                "std": simulation.population.std,
            },
            "primitives": PrimitivesModel(
                ep=WaterServiceCostModel(
                    couts_fixes=simulation.primitives.cost_potable_water.fixed_costs,
                    couts_variables=simulation.primitives.cost_potable_water.variable_costs,
                    number_of_subscribers=simulation.primitives.cost_potable_water.subscribers_number
                ),
                assainissement=WaterServiceCostModel(
                    couts_fixes=simulation.primitives.cost_sanitation.fixed_costs,
                    couts_variables=simulation.primitives.cost_sanitation.variable_costs,
                    number_of_subscribers=simulation.primitives.cost_sanitation.subscribers_number
                ),
                environnement=EnvironmentalModel(
                    couts_fixes_par_an=simulation.primitives.environmental_costs.fixed_costs,
                    couts_variable_moyen=simulation.primitives.environmental_costs.variable_costs,
                ),
                taxation=TaxSectionModel(
                    drinking_water=TaxModel(
                        vat=simulation.primitives.tax_costs.vat_drinking_water,
                        fees=simulation.primitives.tax_costs.fee_drinking_water,
                    ),
                    sanitation=TaxModel(
                        vat=simulation.primitives.tax_costs.vat_sanitation,
                        fees=simulation.primitives.tax_costs.fee_sanitation,
                    )
                ),
                social_data=SocialDataModel(
                    threshold_par=simulation.primitives.social_costs.car_threshold,
                    threshold_car=simulation.primitives.social_costs.par_threshold,
                    poverty=simulation.primitives.social_costs.poverty_threshold,
                    extreme_poverty=simulation.primitives.social_costs.extreme_poverty_threshold
                )
            ),
            "status": simulation.status.value,
            "tariff": TariffModel(
                ep=TariffSectionModel(
                    subscription=simulation.ibt_eau_potable.abonnement,
                    usage_tiers=[
                        ConsumptionThresholds(
                            threshold=b.seuil,
                            price=b.price,
                        )
                        for b in
                        simulation.ibt_eau_potable.blocks
                    ]
                ),
                assainissement=TariffSectionModel(
                    subscription=simulation.ibt_sanitation.abonnement,
                    usage_tiers=[
                        ConsumptionThresholds(
                            threshold=b.seuil,
                            price=b.price,
                        )
                        for b in
                        simulation.ibt_sanitation.blocks
                    ]

                )
            )
        }
    }


@initial_router.get("/simulation/{simulation_id}/tbse_par_plot")
async def get_tbse_par_plot(simulation_id: int, current_user: User = Depends(get_current_active_user),
                            db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    buf = await generate_tbse_par_affordability_plot(simulation)
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/tbse_consumption_plot")
async def get_tbse_consumption_plot(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                    db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    buf = await generate_tbse_consumption_plot(simulation)
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/pens_parade_consumption_plot")
async def get_pens_parade_consumption_plot(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                           db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    buf = await generate_pens_parade_consumptions_plot(simulation)
    return StreamingResponse(buf, media_type="image/png")


@initial_router.get("/simulation/{simulation_id}/consumption_deviation_loses_cost_recovery_plot")
async def get_consumption_deviation_loses_cost_recovery_plot(simulation_id: int,
                                                             current_user: User = Depends(get_current_active_user),
                                                             db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    buf = await generate_consumption_deviation_losses_cost_recovery_plot(simulation)
    return StreamingResponse(buf, media_type="image/png")
