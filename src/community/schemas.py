from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateCommunitySchema(BaseModel):
    name: str = Field(..., description="community name")
    description: Optional[str] = Field(None, description="community description")
    community_header_image: Optional[str] = Field(None, description="community_header_image")
    
    class Config:
        from_attributes = True 
        

class DisplayCommunitySchema(BaseModel):
    id: str 
    name: str 
    description: Optional[str]
    community_header_image: Optional[str]
    date_created: datetime
    
    class Config:
        from_attributes = True 
        

class JoinCommunitySchema(BaseModel):
    associated_user_id: str = Field(..., description="id of user joining")
    associated_community_id: str = Field(..., description="id of the community being joined")
    
    class Config:
        from_attributes = True 
        

class DisplayUserJoinedCommunitiesSchema(BaseModel):
    associated_user_id: str
    associated_community_id: str
    name: str 
    description: Optional[str]
    community_header_image: Optional[str]
    date_joined: datetime
    
    class Config:
        from_attributes = True 