from .models import *
from .schemas import *
from sqlalchemy import select, and_, or_ 
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile, File, Form
import os 
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import json
import bcrypt
from .jwt_handeler import *

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
    user_profile_image: UploadFile = File(..., description="User profile image is required here")    
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


def signup_user(
    db: Session,
    username: str = Form(..., description="username"),
    email: str = Form(..., description="email"),
    password: str = Form(..., description="password"),
    user_profile_image: UploadFile = File(None, description="user profile  image"),
):
    try:
        salt = bcrypt.gensalt(rounds=15)
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
        
        if user_profile_image:
            header_image_url = _upload_header_image_to_cloudinary(user_profile_image)
            
        existing_user_instance = db.execute(select(UserModel).where(UserModel.username == username)).scalar_one_or_none()
        if existing_user_instance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have an account, please log in"
            )
        
        new_user_instance = UserModel(
            username=username,
            email=email,
            password=hashed_password,
            user_profile_image=header_image_url
        )
        
        db.add(new_user_instance)
        db.commit()
        db.refresh(new_user_instance)
        
        return new_user_instance
        
    except Exception as e:
        db.rollback()
        print(f"There was an error trying to signup the new user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to signup the new user: {str(e)}"
        )
        

def signin_user(
    user_data: SigninUserSchema,
    db: Session
) -> UserTokensSchema:
    try:
        existing_user_instance = db.execute(select(UserModel).where(UserModel.username == user_data.username)).scalar_one_or_none()
        if not existing_user_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid credentials used"
            )
            
        checked_password = bcrypt.checkpw(user_data.password.encode("utf-8"), existing_user_instance.password.encode("utf-8"))
        if not checked_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login credentials used cuh, you should not be here actually"
            )
            
        new_user_tokens_data = {
            "sub": existing_user_instance.id,
            "username": existing_user_instance.username
        }
        
        new_user_tokens = generate_user_tokens(new_user_tokens_data)
            
        return new_user_tokens
        
    except Exception as e:
        print(f"There was an error trying to signin the user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to signin the user: {str(e)}"
        )
        

def update_user_profile(
    user_id: str,
    db: Session,
    username: str = Field(None, description='new username'),
    email: str = Field(None, description='new email'),
    password: str = Field(None, description='new password'),
    user_profile_image: UploadFile = File(None, description='new profile image')
):
    try:
        existing_user_instance = db.execute(select(UserModel).where(UserModel.id == user_id))
        
        if not existing_user_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="requested user profile to edit was not found gang 😂"
            )
            
        if username is not None:
            check_unique_username = db.execute(select(UserModel).where(UserModel.username == username)).scalar_one_or_none()
            if check_unique_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New username still has to be unique cuh"
                )
                
            existing_user_instance.username = username 
        if email is not None:
            check_unique_username = db.execute(select(UserModel).where(UserModel.email == email)).scalar_one_or_none()
            if check_unique_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New email still has to be unique cuh"
                )
            existing_user_instance.email = email
            
        if password is not None:
            salt = bcrypt.gensalt(rounds=15)
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
            existing_user_instance.password = hashed_password
            
        if user_profile_image is not None:
            new_image_url = _upload_header_image_to_cloudinary(user_profile_image)
            existing_user_instance.user_profile_image = new_image_url
            
        db.commit()
        db.refresh(existing_user_instance)
        
        return existing_user_instance
        
    except Exception as e:
        db.rollback()
        print(f"There was an error trying to edit the current users profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to edit the current users profile: {str(e)}"
        )