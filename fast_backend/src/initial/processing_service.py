from typing import Optional

import pandas as pd
from sqlalchemy.orm import Session

from src.core.models import Simulation, StatusEnum
from src.initial.schemas import SimulationPayload
from src.small_assessment.new_calculator_service import NewSimulation, save_simulation


async def start_processing_and_calculating_simulation(simulation_id, simulation_payload: SimulationPayload, df: pd.DataFrame,
                                                      db: Session):
    is_g1 = df['Assainissement Collectif (1 = oui)'] == 0
    g1_df = df[is_g1]
    g2_df = df[~is_g1]

    simulator = NewSimulation(simulation_payload, g1_df, g2_df)

    save_simulation(simulation_id, simulator)
    simulation: Optional[Simulation] = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if simulation is None:
        raise Exception("Simulation not found")
    simulation.status = StatusEnum.initialized
    db.add(simulation)
    db.commit()
    return simulation_payload
