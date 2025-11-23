from pydantic import BaseModel, Field
from datetime import datetime

class CreateCommunityPostCommentSchema(BaseModel):
    comment_body: str = Field(..., description="actual contents of the comment")
    
    class Config:
        from_attributes = True 
        

class DisplayCommunityPostCommentSchema(BaseModel):
    id: str 
    associated_community_id: str 
    associated_user_id: str 
    associated_post_id: str 
    commented_body: str 
    date_posted: str 
    
    class Config:
        from_attributes = True 
        
 
 
# if need be, we can make the adjustments so just dont be lazy for no good reason at all   
class EditComminityPostCommentSchema(BaseModel):
    comment_body: str = Field(..., description="new comment body")
    
    class Config:
        from_attributes = True