from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from uuid import uuid4
from ..database import Base

class CommunityModel(Base):
    __tablename__ = "communities"
    
    id = Column(String, primary_key=True, index=True, default=lambda: uuid4().hex)
    associated_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    community_header_image = Column(String, nullable=False)
    date_created = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("UserModel", back_populates="communities")
    joined_communities = relationship("JoinedCommunitiesModel", back_populates="community")
    
    
class JoinedCommunitiesModel(Base):
    __tablename__ = "joined_communities"
    
    id = Column(String, primary_key=True, index=True, default=lambda: uuid4().hex)
    associated_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    associated_community_id = Column(String, ForeignKey("communities.id"), nullable=False)
    date_joined = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    community = relationship("CommunityModel", back_populates="joined_communities")
    user_joined_communities = relationship("UserModel", back_populates="joined_communities")
    