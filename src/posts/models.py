from sqlalchemy import Column, Text, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm  import relationship
from datetime import datetime, timezone
from uuid import uuid4
from ..database import Base


class CommunityPostModel(Base):
    __tablename__ = "community_posts"
    
    id = Column(String, primary_key=True, index=True, default=lambda: uuid4().hex)
    associated_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    associated_community_id = Column(String, ForeignKey("communities.id"), nullable=False)
    post_body = Column(Text, nullable=False)
    post_header_image = Column(String, nullable=True)
    date_posted = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("UserModel", back_populates="user_community_posts")
    community = relationship("CommunityModel", back_populates="community_posts")
    community_post_comments = relationship("CommunityPostCommentModel", back_populates="community_post")