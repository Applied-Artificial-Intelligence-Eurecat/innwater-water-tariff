from sqlalchemy.orm import Session

from src.core.models import IBTEauPotable, BlockEauPotable, IBTSanitation, BlockSanitation, DemandConfiguration, \
    Population, CostsPotableWater, CostsSanitation, EnvironmentalCosts, TaxCosts, SocialCosts, Primitives
from src.initial.schemas import SimulationPayload


async def create_ibt_parameters(db, payload, simulation):
    ibt_potable_water = IBTEauPotable(
        abonnement=payload.tariff.drinking_water.subscription,
        simulation_id=simulation.id
    )
    db.add(ibt_potable_water)
    db.commit()
    for potable_water_block in payload.tariff.drinking_water.usage_tiers:
        db.add(BlockEauPotable(
            seuil=potable_water_block.threshold,
            price=potable_water_block.price,
            ibt_id=ibt_potable_water.id,
        ))
    db.commit()
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
    db.commit()


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
    db.commit()


async def create_population(db, payload: SimulationPayload, simulation):
    population = Population(
        eps=payload.population.eps,
        std=payload.population.std,
        root_database="",
        original_datasource=payload.population.original_datasource,
        database_path=payload.population.bd,
        simulation_id=simulation.id
    )
    db.add(population)
    db.commit()


async def create_primitives(db: Session, payload: SimulationPayload, simulation):
    primitives = Primitives(simulation_id=simulation.id)
    db.add(primitives)
    db.commit()
    potable_water_costs = CostsPotableWater(fixed_costs=payload.primitives.drinking_water.fixed_costs,
                                            variable_costs=payload.primitives.drinking_water.variable_costs,
                                            subscribers_number=payload.primitives.drinking_water.number_of_subscribers,
                                            )
    db.add(potable_water_costs)
    sanitation_costs = CostsSanitation(fixed_costs=payload.primitives.sanitation.fixed_costs,
                                       variable_costs=payload.primitives.sanitation.variable_costs,
                                       subscribers_number=payload.primitives.sanitation.number_of_subscribers)
    db.add(sanitation_costs)
    environmental_costs = EnvironmentalCosts(
        fixed_costs=payload.primitives.environment.fixed_costs_per_year,
        variable_costs=payload.primitives.environment.average_variable_cost
    )
    db.add(environmental_costs)
    tax_costs = TaxCosts(
        vat_drinking_water=payload.primitives.taxation.drinking_water.vat,
        fee_drinking_water=payload.primitives.taxation.drinking_water.fees,
        vat_sanitation=payload.primitives.taxation.sanitation.vat,
        fee_sanitation=payload.primitives.taxation.sanitation.fees
    )
    db.add(tax_costs)
    social_costs = SocialCosts(car_threshold=payload.primitives.social_data.threshold_car,
                               par_threshold=payload.primitives.social_data.threshold_par,
                               poverty_threshold=payload.primitives.social_data.poverty,
                               )
    db.add(social_costs)
    db.commit()
    primitives.potable_water_cost_key = potable_water_costs.id
    primitives.sanitation_cost_key = sanitation_costs.id
    primitives.environmental_cost_key = environmental_costs.id
    primitives.tax_cost_key = tax_costs.id
    primitives.social_cost_key = social_costs.id
    primitives.simulation_id = simulation.id
    db.add(primitives)
    db.commit()
