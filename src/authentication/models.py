from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from uuid import uuid4
from ..database import Base 


class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True, default=lambda: uuid4().hex)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_profile_image = Column(String, nullable=True)
    date_created = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    communities = relationship("CommunityModel", back_populates="user")
    joined_communities = relationship("JoinedCommunitiesModel", back_populates="user_joined_communities")