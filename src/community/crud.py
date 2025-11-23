from .models import *
from .schemas import *
from fastapi import HTTPException, status, UploadFile, File, Form
from ..database import get_db
from sqlalchemy import select, and_, or_ 
from sqlalchemy.orm import Session
from ..authentication.routes import oauth
import os 
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import json

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

def create_new_community(
    user_id: str,
    db: Session,
    name: str = Form(..., description="name of community"),
    description: str = Form(None, description="description of the community"),
    community_header_image: UploadFile = File(None, description="New header image for the community"),
) -> DisplayCommunitySchema:
    try:
        unique_community_name = db.execute(select(CommunityModel).where(CommunityModel.name == name)).scalar_one_or_none()
        if not unique_community_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Community name is supposed to be unique lil bro ☠️"
            )
            
        if community_header_image:
            community_header_image_url = _upload_header_image_to_cloudinary(community_header_image)
            
        new_community_instance = CommunityModel(
            name=name,
            description=description,
            community_header_image=community_header_image_url,
            associated_user_id=user_id
        )
        
        db.add(new_community_instance)
        db.commit()
        db.refresh(new_community_instance)
        
        return new_community_instance
        
    except Exception as e:
        print(f"There was an error trying to create the new community: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to create the new community: {str(e)}"
        )
        
        
def get_all_communities_created(
    db: Session
) -> list[DisplayCommunitySchema]:
    try:
        all_communities = db.execute(select(CommunityModel)).scalars().all()
        
        if not all_communities:
            return []
        
        return all_communities
        
    except Exception as e:
        print(f"There was an error trying to get the communities for you to join: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to get the communities for you to join: {str(e)}"
        )
        


# for the community id we will get it in the url when we click on the join button inside the community
# then for the user_id we get that from the token so it should be fine
def join_community(
    user_id: str,
    community_id: str,
    db: Session
) -> DisplayCommunitySchema:
    try:
        community_instance = db.execute(select(CommunityModel).where(CommunityModel.id == community_id)).scalar_one_or_none()
        if not community_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requested community was not found"
            )
        
        already_joined_instance = db.execute(select(JoinedCommunitiesModel).where(
            and_(
                JoinedCommunitiesModel.associated_user_id == user_id,
                JoinedCommunitiesModel.associated_community_id == community_id
            )
        )).scalar_one_or_none()
        
        if already_joined_instance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already part of this community"
            )
            
        join_new_community = JoinedCommunitiesModel(
            associated_user_id=user_id,
            associated_community_id=community_id
        )
        
        db.add(join_new_community)
        db.commit()
        db.refresh(join_new_community)
        
        return join_new_community
    
    except Exception as e:
        db.rollback()
        print(f"There was an error trying to join this community: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to join this community: {str(e)}"
        )
        

def leave_community(
    user_id: str,
    community_id: str,
    db: Session
):
    try:
        community_instance = db.execute(select(CommunityModel).where(CommunityModel.id == community_id)).scalar_one_or_none()
        if not community_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requested community was not found"
            )
        
        already_joined_instance = db.execute(select(JoinedCommunitiesModel).where(
            and_(
                JoinedCommunitiesModel.associated_user_id == user_id,
                JoinedCommunitiesModel.associated_community_id == community_id
            )
        )).scalar_one_or_none()
        
        if already_joined_instance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already part of this community"
            )
            
        db.delete(already_joined_instance)
        db.commit()
        
        return {
            "message": "You have left the community"
        }
        
    except Exception as e:
        db.rollback()
        print(f"There was ab issue trying to leave the community: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was ab issue trying to leave the community: {str(e)}"
        )
        

def delete_community(
    user_id: str,
    community_id: str,
    db: Session
):
    try:
        community_instance = db.execute(select(CommunityModel).where(
            and_(
                CommunityModel.id == community_id,
                CommunityModel.associated_user_id == user_id
            )    
        )).scalar_one_or_none()
        
        if not community_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requested community was not found"
            )
            
        db.delete(community_instance)
        db.commit()
        
        return { "message": "The community has been deleted" }
        
    except Exception as e:
        db.rollback()
        print(f"There was an error trying to delete the community: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to delete the community: {str(e)}"
        )
      
      
# in case i am not sure we might need to test this endpoint properly to see the data it returns abck to me  
def get_user_joined_communities(
    user_id: str,
    db: Session
) -> list[DisplayCommunitySchema]:
    try:
        user_joined_communities = db.execute(select(JoinedCommunitiesModel).where(JoinedCommunitiesModel.associated_user_id == user_id)).scalars().all()
        
        if not user_joined_communities:
            return []
        
        return user_joined_communities
        
    except Exception as e:
        print(f"There was an error trying to get the users joined communities: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to get the users joined communities: {str(e)}"
        )