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

@router.post("/{community_id}/new", status_code=status.HTTP_201_CREATED, response_model=DisplayCommunityPostSchema)
def create_new_community_post_route(
    community_id:str,
    db: Session = Depends(get_db),
    post_body: str = Form(..., description="post body"),
    post_header_image: UploadFile = File(None, description="Header image if present for the post"),
    current_user_token: str = Depends(oauth)
):
    current_user_details = get_current_user_handeler(current_user_token)
    
    if not current_user_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to be here, please login"
        )
    
    user_id = current_user_details["user_id"]
    
    return upload_new_community_post(
        user_id=user_id,
        community_id=community_id,
        db=db,
        post_body=post_body,
        post_header_image=post_header_image
    )
    

@router.get("/{community_id}", status_code=status.HTTP_200_OK, response_model=list[DisplayCommunityPostSchema])
def display_community_posts_route(
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
    
    return display_all_community_posts(
        user_id=user_id,
        community_id=community_id,
        db=db
    )
    
@router.get("/{community_id}/{post_id}", status_code=status.HTTP_200_OK, response_model=DisplayCommunityPostSchema)
def get_single_community_post_route(
    community_id: str,
    post_id: str,
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
    
    return get_single_community_post(
        user_id=user_id,
        community_id=community_id,
        post_id=post_id,
        db=db
    )
    
@router.delete("/{community_id}/{post_id}")
def delete_community_post_route(
    community_id: str,
    post_id: str,
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
    
    return delete_community_post(
        user_id=user_id,
        community_id=community_id,
        post_id=post_id,
        db=db
    )