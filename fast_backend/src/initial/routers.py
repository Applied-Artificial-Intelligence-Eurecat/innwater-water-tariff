from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from src.core.database import get_db
from src.core.models import User
from src.initial.population_service import generate_population_plot
from src.initial.schemas import PopulationModel
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


@initial_router.post("/presimulation")
async def create_and_save_simulation(payload: SimulationPayload, db: Session = Depends(get_db)):
    user = db.query(User.email).filter(User.email == payload.userid).first()
    if user is None:
        return HTTPException(status_code=404, detail="User not found")
