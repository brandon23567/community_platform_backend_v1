from .models import *
from .crud import *
from .schemas import *
from  ..authentication.routes import oauth
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/community_posts",
    tags=["Community Posts Endpoint"]
)

@router.post("/new", status_code=status.HTTP_201_CREATED)
def create_new_community_post_route():
    return