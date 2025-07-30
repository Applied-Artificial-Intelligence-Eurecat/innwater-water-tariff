from src.core.models import IBTEauPotable, BlockEauPotable, IBTSanitation, BlockSanitation, DemandConfiguration, \
    Population, CostsPotableWater, CostsSanitation, EnvironmentalCosts, TaxCosts, SocialCosts, Primitives


async def create_ibt_parameters(db, payload, simulation):
    ibt_potable_water = IBTEauPotable(
        abonnement=payload.tariff.drinking_water.subscription,
        simulation_id=simulation.id
    )
    db.add(ibt_potable_water)
    for potable_water_block in payload.tariff.drinking_water.usage_tiers:
        db.add(BlockEauPotable(
            seuil=potable_water_block.threshold,
            price=potable_water_block.price,
            ibt_id=ibt_potable_water.id,
        ))
    ibt_sanitation = IBTSanitation(
        abonnement=payload.tariff.sanitation.subscription,
        simulation_id=simulation.id
    )
    db.add(ibt_sanitation)
    for sanitation_block in payload.tariff.sanitation.usage_tiers:
        db.add(BlockSanitation(
            seuil=sanitation_block.threshold,
            price=sanitation_block.price,
            ibt_id=ibt_sanitation.id,
        ))


async def create_demand(db, payload, simulation):
    demand_configuration = DemandConfiguration(
        a=payload.demand.coefficients.a0,
        b=payload.demand.coefficients.a1,
        c=payload.demand.coefficients.a2,
        d=payload.demand.coefficients.a3,
        e=payload.demand.coefficients.a4,
        f=payload.demand.coefficients.a5,
        g=payload.demand.coefficients.a6,
        perception_parameter=payload.demand.k,
        pool=payload.demand.has_pool,
        garden=payload.demand.has_garden,
        simulation_id=simulation.id
    )
    db.add(demand_configuration)


async def create_population(db, payload, simulation):
    population = Population(
        eps=payload.population.eps,
        std=payload.population.std,
        root_database=payload.population.root_database,
        database_path=payload.population.database_path,
        simulation_id=simulation.id
    )
    db.add(population)


async def create_primitives(db, payload, simulation):
    potable_water_costs = CostsPotableWater(fixed_costs=payload.primitives.drinking_water.fixed_costs,
                                            variable_costs=payload.primitives.drinking_water.variable_costs,
                                            subscribers_number=payload.primitives.drinking_water.number_of_subscribers)
    db.add(potable_water_costs)
    sanitation_costs = CostsSanitation(fixed_costs=payload.primitives.sanitation.fixed_costs,
                                       variable_costs=payload.primitives.sanitation.variable_costs,
                                       subscribers_number=payload.primitives.sanitation.number_of_subscribers)
    db.add(sanitation_costs)
    environmental_costs = EnvironmentalCosts(
        fixed_costs=payload.primitives.environment.fixed_costs,
        variable_costs=payload.primitives.environment.variable_costs
    )
    db.add(environmental_costs)
    tax_costs = TaxCosts(
        vat_drinking_water=payload.primitives.taxation.drinking_water.vat,
        fee_drinking_water=payload.primitives.taxation.drinking_water.fee,
        vat_sanitation=payload.primitives.taxation.sanitation.vat,
        fee_sanitation=payload.primitives.taxation.sanitation.fee
    )
    db.add(tax_costs)
    social_costs = SocialCosts(car_threshold=payload.primitives.social_data.car_threshold,
                               par_threshold=payload.primitives.social_data.par_threshold,
                               poverty_threshold=payload.primitives.social_data.poverty,
                               extreme_poverty_threshold=payload.primitives.social_data.extreme_poverty
                               )
    db.add(social_costs)
    primitives = Primitives(
        potable_water_cost_key=potable_water_costs.id,
        sanitation_cost_key=sanitation_costs.id,
        environmental_cost_key=environmental_costs.id,
        tax_cost_key=tax_costs.id,
        social_cost_key=social_costs.id,
        simulation_id=simulation.id
    )
    db.add(primitives)
