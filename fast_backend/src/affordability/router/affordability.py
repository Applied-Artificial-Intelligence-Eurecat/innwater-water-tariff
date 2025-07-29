from typing import Dict, List, Union, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db

router = APIRouter(
    prefix="/api/affordability",
    tags=["affordability"],
    responses={404: {"description": "Not found"}},
)
