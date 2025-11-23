from .models import *
from .crud import *
from .schemas import *
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Depends
from fastapi.security import    OAuth2PasswordBearer
from .jwt_handeler import *

oauth = OAuth2PasswordBearer(tokenUrl="/signin", description="Main auth token for current logged in user")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=DisplayUserSchema)
def signup_user_route(
    db: Session = Depends(get_db),
    username: str = Form(..., description="username"),
    email: str = Form(..., description="email"),
    password: str = Form(..., description="password"),
    user_profile_image: UploadFile = File(None, description="user profile  image")
):
    return signup_user(
        db=db,
        username=username,
        email=email,
        password=password,
        user_profile_image=user_profile_image
    )
    
    
@router.post("/signin", status_code=status.HTTP_200_OK, response_model=UserTokensSchema)
def signin_user_route(
    user_data: SigninUserSchema,
    db: Session = Depends(get_db)
):
    return signin_user(
        user_data=user_data,
        db=db
    )
    

@router.get("/me", status_code=status.HTTP_200_OK, response_model=DisplayUserSchema)
def get_current_user_route(
    current_user_token: str = Depends(oauth)
):
    current_user_details = get_current_user_handeler(current_user_token)
    
    user_id = current_user_details["user_id"]
    username = current_user_details["username"]
    
    return {
        "user_id": user_id,
        "username": username
    }
    

@router.post("/refresh_token", status_code=status.HTTP_201_CREATED, response_model=UserTokensSchema)
def refresh_tokens_route(
    refresh_token: str,
    current_user_token: str = Depends(oauth)
):
    current_user_details = get_current_user_handeler(current_user_token)
    
    if not current_user_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to be here, please login"
        )
    
    user_id = current_user_details["user_id"]
    username = current_user_details["username"]
    
    new_refreshed_tokens = refresh_access_token(refresh_token)
    
    return new_refreshed_tokens

@router.put("/{user_id}/update", status_code=status.HTTP_200_OK, response_model=DisplayUserSchema)
def update_user_profile_route(
    db: Session = Depends(get_db),
    username: str = Form(None, description='new username'),
    email: str = Form(None, description='new email'),
    password: str = Form(None, description='new password'),
    user_profile_image: UploadFile = File(None, description='new profile image'),
    current_user_token: str = Depends(oauth)
):
    current_user_details = get_current_user_handeler(current_user_token)
    
    if not current_user_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to be here, please login"
        )
    
    user_id = current_user_details["user_id"]
    
    return update_user_profile(
        user_id=user_id,
        db=db,
        username=username,
        email=email,
        password=password,
        user_profile_image=user_profile_image
    )