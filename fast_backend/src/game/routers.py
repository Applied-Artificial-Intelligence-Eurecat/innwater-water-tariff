from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.core.auth import get_current_active_user
from src.core.database import get_db
from src.core.models import User, GameRound, GameParticipant, Simulation
from src.game.schemas import RoundSchema, ParticipationSchema, ParticipationRound, RoundSchemaResponse
from src.initial.routers import get_simulation_payload_from_db
from src.results.routers import calculate_rex
from src.small_assessment.affordability_service import affordability_general
from src.small_assessment.incentive_service import incentive_effect_consumption
from src.small_assessment.new_calculator_service import get_or_create_simulation_from_payload

game_router = APIRouter(prefix="/game",
                        tags=["game"],
                        responses={404: {"description": "Not found"}},
                        )


@game_router.post("/round/new")
async def create_new_round(round: RoundSchema, current_user: User = Depends(get_current_active_user),
                           db: Session = Depends(get_db)):
    game_round = GameRound(alpha=round.alpha, ratio_tbse=round.ratio_tbse, threshold_res=round.threshold_res)
    db.add(game_round)
    db.commit()
    return {"id": game_round.id}


@game_router.get("/round/")
async def get_rounds(db: Session = Depends(get_db)):
    game_rounds = db.query(GameRound).all()
    return [
        RoundSchemaResponse(
            round_id=game_round.id,
            alpha=float(game_round.alpha),
            ratio_tbse=float(game_round.ratio_tbse),
            threshold_res=float(game_round.threshold_res))
        for game_round in game_rounds
    ]


@game_router.delete("/round/{game_round_id}")
async def delete_round(game_round_id: int, current_user: User = Depends(get_current_active_user),
                       db: Session = Depends(get_db)):
    db.query(GameRound).filter(GameRound.id == game_round_id).delete()
    db.commit()


@game_router.get("/round/{game_round_id}/participation/{simulation_id}")
async def link_round_to_simulation(game_round_id: int, simulation_id: int,
                                   current_user: User = Depends(get_current_active_user),
                                   db: Session = Depends(get_db)):
    game_round = db.query(GameRound).filter(GameRound.id == game_round_id).first()
    if game_round is None:
        raise HTTPException(status_code=404, detail="Game round not found")
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not ofound not found")
    game_participant = db.query(GameParticipant).filter(GameParticipant.game_round_id == game_round_id,
                                                        GameParticipant.simulation_id == simulation_id).first()
    if game_participant:
        raise HTTPException(status_code=400, detail="Game participant already exists")

    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    calculation = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)

    rex_value = (await calculate_rex(calculation))['total_cost']
    if abs(rex_value) > game_round.threshold_res:
        score = 9999999999999999
    else:
        general_ieffect = incentive_effect_consumption(calculation)
        targeted_consumption_level = general_ieffect.mean.tbse * game_round.ratio_tbse
        squared_error = (targeted_consumption_level - general_ieffect.mean.ibt) ** 2
        right_part = game_round.alpha * squared_error
        left_part = affordability_general(calculation).aparent_deficit.ibt * (1 - game_round.alpha)
        score = right_part + left_part

    simulation.status = "completed"
    game_participant = GameParticipant(game_round_id=game_round_id, simulation_id=simulation_id, game_score=score, )
    db.add(game_participant)
    db.add(simulation)
    db.commit()
    return {"score": score}


@game_router.get("/round/{game_round_id}/participations")
async def get_round_participation(game_round_id: int,
                                  current_user: User = Depends(get_current_active_user),
                                  db: Session = Depends(get_db)):
    game_participant = db.query(GameParticipant).filter(GameParticipant.game_round_id == game_round_id).order_by(
        desc(GameParticipant.game_score), ).all()
    if game_participant is None:
        raise HTTPException(status_code=404, detail="Game participant not found")

    res = []
    for game_part in game_participant:
        simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == game_part.simulation_id).first()
        if simulation is None:
            continue
        res.append(ParticipationSchema(round_id=int(game_part.game_round_id), simulation_name=simulation.name,
                                       score=float(game_part.game_score)))

    return res


@game_router.get("/{simulation_id}/participations")
async def get_participations(simulation_id: int,
                             current_user: User = Depends(get_current_active_user),
                             db: Session = Depends(get_db)):
    game_participant = db.query(GameParticipant).filter(GameParticipant.simulation_id == simulation_id).all()
    if game_participant is None:
        raise HTTPException(status_code=404, detail="Game participant not found")
    res = []
    for game_part in game_participant:
        simulation: Simulation | None = db.query(Simulation).filter(Simulation.id == game_part.simulation_id).first()
        if simulation is None:
            continue
        game_round: GameRound | None = db.query(GameRound).filter(GameRound.id == game_part.game_round_id).first()
        if game_round is None:
            continue
        res.append(ParticipationRound(
            round_id=game_round.id,
            alpha=float(game_round.alpha),
            ratio_tbse=float(game_round.ratio_tbse),
            threshold_res=float(game_round.threshold_res),
            simulation_name=simulation.name,
            score=float(game_part.game_score)))
    return res


@game_router.get("/{simulation_id}/non_participations")
async def get_non_participations(simulation_id: int,
                                 current_user: User = Depends(get_current_active_user),
                                 db: Session = Depends(get_db)):
    game_participant = db.query(GameParticipant).filter(GameParticipant.simulation_id == simulation_id).all()
    if game_participant is None:
        raise HTTPException(status_code=404, detail="Game participant not found")
    rounds = db.query(GameRound).all()
    res = []
    for round in rounds:
        if round.id in [game_part.game_round_id for game_part in game_participant]:
            continue
        res.append(RoundSchema(alpha=float(round.alpha), ratio_tbse=float(round.ratio_tbse),
                               threshold_res=float(round.threshold_res), ))
    return res
