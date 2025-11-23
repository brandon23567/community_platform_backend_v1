from .schemas import *
from .models import *
from ..authentication.models import * 
from ..authentication.routes import *
from ..community.models import *
from ..posts.models import *
from fastapi import HTTPException, status, Depends, Form
from sqlalchemy import select, and_, or_ 
from sqlalchemy.orm import Session

def upload_new_comment(
    user_id: str,
    community_id: str,
    post_id: str,
    comment_data: CreateCommunityPostCommentSchema,
    db: Session
):
    try:
        existing_joined_community_instance = db.execute(select(JoinedCommunitiesModel).where(
            and_(
                JoinedCommunitiesModel.associated_community_id == community_id,
                JoinedCommunitiesModel.associated_user_id == user_id
            )
        )).scalar_one_or_none()
        
        if not existing_joined_community_instance:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You cannot delete posts to a community you have not joined"
            )
            
        new_post_comment_instance = CommunityPostCommentModel(
            associated_user_id=user_id,
            associated_community_id=community_id,
            associated_post_id=post_id,
            comment_body=comment_data.comment_body
        )
        
        db.add(new_post_comment_instance)
        db.commit()
        
        db.refresh(new_post_comment_instance)
        
        return new_post_comment_instance
        
    except Exception as e:
        db.rollback()
        print(f"There was an error trying to upload the comment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to upload the comment: {str(e)}"
        )
        

def edit_post_comment(
    user_id: str,
    community_id: str,
    post_id: str,
    comment_data: EditComminityPostCommentSchema,
    db: Session
):
    try:
        existing_joined_community_instance = db.execute(select(JoinedCommunitiesModel).where(
            and_(
                JoinedCommunitiesModel.associated_community_id == community_id,
                JoinedCommunitiesModel.associated_user_id == user_id
            )
        )).scalar_one_or_none()
        
        if not existing_joined_community_instance:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You cannot delete posts to a community you have not joined"
            )
            
        existing_post_comment_instance = db.execute(select(CommunityPostCommentModel).where(
            and_(
                CommunityPostCommentModel.associated_community_id == community_id,
                CommunityPostCommentModel.associated_user_id == user_id,
                CommunityPostCommentModel.associated_post_id == post_id
            )
        )).scalar_one_or_none()
        
        if not existing_post_comment_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requested post commented to edit was not found ☠️"
            )
            
        if comment_data.comment_body is not None:
            existing_post_comment_instance.comment_body = comment_data.comment_body
            
        db.commit()
        db.refresh(existing_post_comment_instance)
        
        return existing_post_comment_instance
        
    except Exception as e:
        print(f"There was an error trying to edit this comment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to edit this comment: {str(e)}"
        )
        

def delete_community_post_comment(
    user_id: str,
    community_id: str,
    post_id: str,
    db: Session
):
    try:
        existing_joined_community_instance = db.execute(select(JoinedCommunitiesModel).where(
            and_(
                JoinedCommunitiesModel.associated_community_id == community_id,
                JoinedCommunitiesModel.associated_user_id == user_id
            )
        )).scalar_one_or_none()
        
        if not existing_joined_community_instance:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You cannot delete posts to a community you have not joined"
            )
            
        comment_instance_to_delete = db.execute(select(CommunityPostCommentModel).where(
            and_(
                CommunityPostCommentModel.associated_community_id == community_id,
                CommunityPostCommentModel.associated_post_id == post_id,
                CommunityPostCommentModel.associated_user_id == user_id
            )
        )).scalar_one_or_none()
        
        if not comment_instance_to_delete:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are unable to delete this comment on this post, sorry 😂"
            )
            
        db.delete(comment_instance_to_delete)
        db.commit()
        
        return { "message": "Comment has been deleted" }
        
    except Exception as e:
        db.rollback()
        print(f"There was an error trying to delete the post commnet: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to delete the post commnet: {str(e)}"
        )