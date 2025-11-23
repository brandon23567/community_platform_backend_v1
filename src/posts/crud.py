from .models import *
from .schemas import *
from fastapi import HTTPException, status, UploadFile, Form, File
from sqlalchemy import select, and_ 
from sqlalchemy.orm  import Session
from ..authentication.jwt_handeler import *
import os 
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import json
from ..community.models import *

load_dotenv()

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD_NAME,
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET
)

if not CLOUDINARY_CLOUD_NAME or not CLOUDINARY_API_KEY or not CLOUDINARY_API_SECRET:
    raise ValueError("Unable to form a connection to cloudinary for image uploads")


def _upload_header_image_to_cloudinary(
    user_profile_image: UploadFile = File(..., description="community header image required here")    
) -> str:
    try:
        image_url = cloudinary.uploader.upload(
            user_profile_image.file,
            use_filename=True,
            unique_filename=True
        )
        
        image_secure_url = json.loads(image_url)["secure_url"]
        
        return image_secure_url
        
    except Exception as e:
        print(f"There was an error uploading the image to cloudinary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error uploading the image to cloudinary: {str(e)}"
        )
        
        
def upload_new_community_post(
    user_id: str,
    community_id: str,
    db: Session,
    post_body: str = Form(..., description="post body"),
    post_header_image: UploadFile = File(None, description="Header image if present for the post")
) -> DisplayCommunityPostSchema:
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
                detail="You cannot upload a post to a community you have not joined"
            )
            
        if post_header_image:
            post_header_image_url = _upload_header_image_to_cloudinary(post_header_image)
            
            new_community_post_instance = CommunityPostModel(
                post_body=post_body,
                post_header_image=post_header_image_url,
                associated_user_id=user_id,
                associated_community_id=community_id
            )
            
            db.add(new_community_post_instance)
            db.commit()
            
            db.refresh(new_community_post_instance)
            
            return new_community_post_instance
        
        new_community_post_instance = CommunityPostModel(
            post_body=post_body,
            associated_user_id=user_id,
            associated_community_id=community_id
        )
            
        db.add(new_community_post_instance)
        db.commit()
            
        db.refresh(new_community_post_instance)
            
        return new_community_post_instance
        
    except Exception as e:
        db.rollback()
        print(f"There was an error trying to upload the new post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to upload the new post: {str(e)}"
        )
        

def display_all_community_posts(
    user_id: str,
    community_id: str,
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
                detail="You cannot view posts to a community you have not joined"
            )
            
        community_posts = db.execute(select(CommunityPostModel).where(CommunityPostModel.associated_community_id == community_id)).scalars().all()
        
        if not community_posts:
            return []
        
        return community_posts
        
    except Exception as e:
        print(f"There was an error trying to get the community posts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to get the community posts: {str(e)}"
        )
        

def get_single_community_post(
    user_id: str,
    community_id: str,
    post_id: str,
    db: Session
) -> DisplayCommunityPostSchema:
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
                detail="You cannot view posts to a community you have not joined"
            )
            
        requested_post_instance = db.execute(select(CommunityPostModel).where(
            and_(
                CommunityPostModel.id == post_id,
                CommunityPostModel.associated_community_id == community_id
            )
        )).scalar_one_or_none()
        
        if not requested_post_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requested post details was nto found ☠️"
            )
            
        return requested_post_instance
        
    except Exception as e:
        print(f"There was an error trying to get this single post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to get this single post: {str(e)}"
        )
        

def delete_community_post(
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
            
        post_to_delete_instance = db.execute(select(CommunityPostModel).where(
            and_(
                CommunityPostModel.id == post_id,
                CommunityPostModel.associated_community_id == community_id,
                CommunityPostModel.associated_user_id == user_id
            )
        )).scalar_one_or_none()
        
        if not post_to_delete_instance:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are unable to delete this specific post"
            )
            
        db.delete(post_to_delete_instance)
        db.commit()
        
        return { "message": "Post has been deleted gang 🗿" }
        
    except Exception as e:
        db.rollback()
        print(f"There was an error trying to delete the community post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to delete the community post: {str(e)}"
        )