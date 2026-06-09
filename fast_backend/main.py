import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.database import engine, Base
from src.game.routers import game_router
from src.initial.routers import initial_router
from src.results.routers import results_router
from src.small_assessment.routers import small_assessment_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables in the database
    Base.metadata.create_all(bind=engine)
    yield


# Create FastAPI app
app = FastAPI(
    title="Water Tariff API",
    description="API for water tariff calculations and affordability indicators",
    version="1.0.0",
    root_path="/water-tariff-api/api/v1",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(initial_router)
app.include_router(small_assessment_router)
app.include_router(results_router)

app.include_router(game_router)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn

    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    # Run the application
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
