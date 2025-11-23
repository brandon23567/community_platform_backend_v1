from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UploadCommunityPostSchema(BaseModel):
    post_body: str = Field(..., description="actual text content of the post")
    post_header_image: Optional[str] = Field(None, description="If there is an image associated with the post")
    associated_user_id: str = Field(..., description="user who is posting this")
    associated_community_id: str = Field(..., description="community where post is going")
    
    class Config:
        from_attributes = True
        

class DisplayCommunityPostSchema(BaseModel):
    id: str 
    post_body: str
    post_header_image: Optional[str]
    associated_user_id: str
    associated_community_id: str
    date_posted: datetime
    
    class Config:
        from_attributes = True