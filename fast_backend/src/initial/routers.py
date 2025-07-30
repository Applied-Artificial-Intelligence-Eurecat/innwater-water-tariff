from datetime import timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from src.core.auth import authenticate_user, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, \
    get_current_active_user
from src.core.database import get_db
from src.core.models import User, Simulation, Project, StatusEnum
from src.initial.initial_service import create_ibt_parameters, create_demand, create_population, create_primitives
from src.initial.population_service import generate_population_plot
from src.initial.schemas import PopulationModel, UserCreate, Token
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
        project = Project(project_id=0, name="Default Project", user_id=current_user.id)
        db.add(project)
    simulation = Simulation(
        name=payload.launch.simulation_name,
        number_of_periods=payload.launch.periods,
        status=StatusEnum.initialized,
        project_id=project.project_id
    )
    db.add(simulation)
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


