from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.auth import get_current_active_user
from src.core.database import get_db
from src.core.models import User, Simulation, Project, StatusEnum, BlockEauPotable, BlockSanitation
from src.initial.routers import create_tariff_model_payload_from_simulation
from src.initial.schemas import TariffModel

small_assessment_router = APIRouter(
    prefix="/small_assessment",
    tags=["small_assessment"],
    responses={404: {"description": "Not found"}},
)


@small_assessment_router.get("/ibt/{simulation_id}", response_model=TariffModel)
async def get_ibt_parameters(simulation_id, current_user: User = Depends(get_current_active_user),
                             db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")

    return await create_tariff_model_payload_from_simulation(simulation)


@small_assessment_router.put("/ibt/{simulation_id}", response_model=TariffModel)
async def update_ibt_parameters(simulation_id, payload: TariffModel,
                                current_user: User = Depends(get_current_active_user),
                                db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    if simulation.status != StatusEnum.initialized:
        raise HTTPException(status_code=400, detail="Simulation is not initialized")
    simulation.ibt_eau_potable.abonnement = payload.drinking_water.subscription
    drinking_water_blocks = []
    for block in payload.drinking_water.usage_tiers:
        drinking_water_block = BlockEauPotable(
            seuil=block.threshold,
            price=block.price,
            ibt_id=simulation.ibt_eau_potable.id,
        )
        db.add(drinking_water_block)
        db.commit()
        drinking_water_blocks.append(drinking_water_block)
    simulation.ibt_eau_potable.blocks = drinking_water_blocks
    db.add(simulation.ibt_eau_potable)
    db.commit()

    simulation.ibt_sanitation.abonnement = payload.sanitation.subscription
    sanitation_blocks = []
    for block in payload.sanitation.usage_tiers:
        sanitation_block = BlockSanitation(
            seuil=block.threshold,
            price=block.price,
            ibt_id=simulation.ibt_sanitation.id,
        )
        db.add(sanitation_block)
        db.commit()
        sanitation_blocks.append(sanitation_block)
    simulation.ibt_sanitation.blocks = sanitation_blocks
    db.add(simulation.ibt_sanitation)
    db.commit()

    db.add(simulation)
    db.commit()

    # TODO: Here, we must compute again the dashboard @jimmy

    return await create_tariff_model_payload_from_simulation(simulation)


async def check_simulation_ibt_is_updated(simulation: Simulation, payload: TariffModel) -> bool:
    if simulation.ibt_eau_potable.abonnement != payload.drinking_water.subscription:
        return False
    if simulation.ibt_sanitation.abonnement != payload.sanitation.subscription:
        return False

    for payload_block, simulation_block in zip(payload.drinking_water.usage_tiers, simulation.ibt_eau_potable.blocks):
        if payload_block.threshold != simulation_block.seuil:
            return False
        if payload_block.price != simulation_block.price:
            return False

    for payload_block, simulation_block in zip(payload.sanitation.usage_tiers, simulation.ibt_sanitation.blocks):
        if payload_block.threshold != simulation_block.seuil:
            return False
        if payload_block.price != simulation_block.price:
            return False
    return True


@small_assessment_router.post("/validate/{simulation_id}")
async def validate_and_evaluate(simulation_id, payload: TariffModel,
                                current_user: User = Depends(get_current_active_user),
                                db: Session = Depends(get_db)):
    simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == simulation_id).join(Project).filter(
        Project.user_id == current_user.id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    is_ok = await check_simulation_ibt_is_updated(simulation, payload)
    if not is_ok:
        return {
            "status": "error",
            "message": "Simulation update failed, check IBT parameters are updated."
        }

    simulation.status = StatusEnum.first_evaluation
    db.add(simulation)
    db.commit()

    # TODO: Start full evaluation @jimmy

    return {
        "status": "success",
        "message": "Simulation updated successfully"
    }

