from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class CreateUserSchema(BaseModel):
    username: str = Field(..., description="username")
    email: EmailStr = Field(..., description="email")
    password: str = Field(..., description="password")
    user_profile_image: Optional[str] = Field(None, description="user profile image")
    
    class Config:
        from_attributes = True
        

class SigninUserSchema(BaseModel):
    username: str = Field(..., description="username")
    password: str = Field(..., description="password")
    
    class Config:
        from_attributes = True
        

class UserTokensSchema(BaseModel):
    access_token: str = Field(..., description="access token")
    refresh_token: str = Field(..., description="user refresh token")
    
    class Config:
        from_attributes = True        
        
class EditUserSchema(BaseModel):
    username: str = Field(None, description="new username")
    email: EmailStr = Field(None, description="new updated email")
    password: str = Field(None, description="New updated password")
    user_profile_image: str = Field(None, description="New user profile image")
    
    class Config:
        from_attributes = True
        

class DisplayUserSchema(BaseModel):
    id: str 
    username: str 
    email: EmailStr
    user_profile_image: Optional[str]
    
    class Config:
        from_attributes = True 