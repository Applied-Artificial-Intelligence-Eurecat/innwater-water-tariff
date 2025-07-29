from typing import Optional

from sqlalchemy.orm import Session

from src.core.models import (
    Simulation, Primitives, Population, DemandConfiguration,
    IBTEauPotable, BlockEauPotable, IBTSanitation, BlockSanitation,
    StatusEnum, Project
)
from src.initial.schemas import SimulationPayload


async def save_simulation_schema(schema: SimulationPayload, db: Session) -> Optional[int]:
    """
    Takes a simulation schema and saves it to the database.
    
    Args:
        schema: The simulation payload containing all simulation data
        db: Database session
        
    Returns:
        int: The ID of the newly created simulation record, or None if the operation failed
    """
    try:
        # Get the project for the user
        project: Optional[Project] = db.query(Project).filter(Project.user_id == schema.userid).first()
        if not project:
            # Handle case where project doesn't exist
            return None

        # Create new simulation record
        simulation = Simulation(
            name=schema.launch.simulation_name,
            number_of_periods=schema.launch.periods,
            status=StatusEnum.created,
            project_id=int(project.project_id),
        )
        db.add(simulation)
        db.flush()  # Flush to get the simulation ID

        # Save primitives
        if schema.primitives:
            primitives = Primitives(
                environmental_costs=schema.primitives.environment.fixed_costs_per_year if schema.primitives.environment else None,
                social_data=str(schema.primitives.social_data.model_dump_json()) if schema.primitives.social_data else None,
                fiscalite=str(schema.primitives.taxation.model_dump_json()) if schema.primitives.taxation else None,
                simulation_id=simulation.id
            )
            db.add(primitives)

        # Save population
        if schema.population:
            population = Population(
                eps=schema.population.eps,
                std=schema.population.std,
                simulation_id=simulation.id
            )
            db.add(population)

        # Save demand configuration
        if schema.demand:
            demand_config = DemandConfiguration(
                a=schema.demand.coefficients.a0 if schema.demand.coefficients else None,
                b=schema.demand.coefficients.a1 if schema.demand.coefficients else None,
                c=schema.demand.coefficients.a2 if schema.demand.coefficients else None,
                d=schema.demand.coefficients.a3 if schema.demand.coefficients else None,
                e=schema.demand.coefficients.a4 if schema.demand.coefficients else None,
                f=schema.demand.coefficients.a5 if schema.demand.coefficients else None,
                g=schema.demand.coefficients.a6 if schema.demand.coefficients else None,
                perception_parameter=schema.demand.k,
                piscine=schema.demand.has_pool,
                jardin=schema.demand.has_garden,
                simulation_id=simulation.id
            )
            db.add(demand_config)

        # Save tariff information - Drinking Water
        if schema.tariff and schema.tariff.drinking_water:
            ibt_eau = IBTEauPotable(
                abonnement=str(schema.tariff.drinking_water.subscription),
                simulation_id=simulation.id
            )
            db.add(ibt_eau)
            db.flush()  # Flush to get the IBT ID

            # Save blocks for drinking water
            if schema.tariff.drinking_water.usage_tiers:
                for tier in schema.tariff.drinking_water.usage_tiers:
                    block = BlockEauPotable(
                        seuil=tier.threshold,
                        price=tier.price,
                        ibt_id=ibt_eau.id
                    )
                    db.add(block)

        # Save tariff information - Sanitation
        if schema.tariff and schema.tariff.sanitation:
            ibt_sanitation = IBTSanitation(
                abonnement=str(schema.tariff.sanitation.subscription),
                simulation_id=simulation.id
            )
            db.add(ibt_sanitation)
            db.flush()  # Flush to get the IBT ID

            # Save blocks for sanitation
            if schema.tariff.sanitation.usage_tiers:
                for tier in schema.tariff.sanitation.usage_tiers:
                    block = BlockSanitation(
                        seuil=tier.threshold,
                        price=tier.price,
                        ibt_id=ibt_sanitation.id
                    )
                    db.add(block)

        # Commit all changes
        db.commit()
        return simulation.id

    except Exception as e:
        db.rollback()
        print(f"Error saving simulation schema to database: {str(e)}")
        return None
