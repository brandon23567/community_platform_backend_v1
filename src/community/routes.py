from .models import *
from .schemas import *
from .crud import *
from ..authentication.routes import oauth
from ..authentication.jwt_handeler import *
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import HTTPException, status, Depends, UploadFile, File, Form, APIRouter


router = APIRouter(
    prefix="/communities",
    tags=["Community Endpoint"]
)


@router.post("/new", status_code=status.HTTP_201_CREATED)
def create_new_community_route(
    db: Session = Depends(get_db),
    name: str = Form(..., description="name of community"),
    description: str = Form(None, description="description of the community"),
    community_header_image: UploadFile = File(None, description="New header image for the community"),
    current_user_token: str = Depends(oauth)
):
    current_user_details = get_current_user_handeler(current_user_token)
    
    if not current_user_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to be here, please login"
        )
    
    user_id = current_user_details["user_id"]
    
    return create_new_community(
        user_id=user_id,
        db=db,
        name=name,
        description=description,
        community_header_image=community_header_image
    )
    

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_communities_route(
    db: Session = Depends(get_db),
    current_user_token: str = Depends(oauth)
):
    current_user_details = get_current_user_handeler(current_user_token)
    
    if not current_user_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to be here, please login"
        )
        
    return get_all_communities_created(db=db)


@router.post("/{community_id}/join", status_code=status.HTTP_201_CREATED)
def join_community_route(
    community_id: str,
    db: Session = Depends(get_db),
    current_user_token: str = Depends(oauth)
):
    current_user_details = get_current_user_handeler(current_user_token)
    
    if not current_user_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to be here, please login"
        )
    
    user_id = current_user_details["user_id"]
    
    return join_community(
        user_id=user_id,
        community_id=community_id,
        db=db
    )
    

@router.post("/{community_id}/leave", status_code=status.HTTP_200_OK)
def leave_community_route(
    community_id: str,
    db: Session = Depends(get_db),
    current_user_token: str = Depends(oauth)
):
    current_user_details = get_current_user_handeler(current_user_token)
    
    if not current_user_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to be here, please login"
        )
    
    user_id = current_user_details["user_id"]
    
    return leave_community(
        user_id=user_id,
        community_id=community_id,
        db=db
    )
    

@router.delete("/{community_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_community_route(
    community_id: str,
    db: Session = Depends(get_db),
    current_user_token: str = Depends(oauth)
):
    current_user_details = get_current_user_handeler(current_user_token)
    
    if not current_user_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to be here, please login"
        )
    
    user_id = current_user_details["user_id"]
    
    return delete_community(
        user_id=user_id,
        community_id=community_id,
        db=db
    )
    

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_communities_route(
    db: Session = Depends(get_db),
    current_user_token: str = Depends(oauth)
):
    current_user_details = get_current_user_handeler(current_user_token)
    
    if not current_user_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to be here, please login"
        )
    
    user_id = current_user_details["user_id"]
    
    return get_user_joined_communities(
        user_id=user_id,
        db=db
    )