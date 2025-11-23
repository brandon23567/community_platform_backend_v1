from .crud import *
from .schemas import *
from .models import *
from ..authentication.routes import oauth
from fastapi import APIRouter, HTTPException, Depends, status, Form
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/community_comments",
    tags=["Community Comments Endpoint"]
)

@router.post("/{community_id}/post/{post_id}}", status_code=status.HTTP_201_CREATED)
def create_new_community_post_comment_route(
    community_id: str,
    post_id: str,
    comment_data: CreateCommunityPostCommentSchema,
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
    
    return upload_new_comment(
        user_id=user_id,
        community_id=community_id,
        post_id=post_id,
        comment_data=comment_data,
        db=db
    )
    
@router.put("{community_id}/edit_comment/{post_id}", status_code=status.HTTP_200_OK)
def edit_community_post_comment_route(
    community_id: str,
    post_id: str,
    comment_data: CreateCommunityPostCommentSchema,
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
    
    return edit_post_comment(
        user_id=user_id,
        community_id=community_id,
        post_id=post_id,
        comment_data=comment_data,
        db=db
    )
    
@router.delete("/{community_id}/{post_id}")
def delete_comunity_post_comment(
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
    
    return delete_community_post_comment(
        user_id=user_id,
        community_id=community_id,
        post_id=post_id,
        db=db
    )