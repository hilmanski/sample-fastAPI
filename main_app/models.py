from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)

    team = relationship("Team", back_populates="members")

class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    members = relationship("Member", back_populates="team")
