from sqlalchemy import Column, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm  import relationship
from datetime import datetime
from uuid import uuid4
from ..database import Base
from datetime import datetime, timezone

class CommunityPostCommentModel(Base):
    __tablename__ = "community_posts_comment"
    
    id = Column(String, primary_key=True, index=True, default=lambda: uuid4().hex)
    associated_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    associated_community_id = Column(String, ForeignKey("communities.id"), nullable=False)
    associated_post_id = Column(String, ForeignKey("community_posts.id"), nullable=False)
    comment_body = Column(Text, nullable=False)
    date_posted = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("UserModel", back_populates="user_posts_comments")
    community_post = relationship("CommunityPostModel", back_populates="community_post_comments")