from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel

from main_app.database import Base


class MemberBase(BaseModel):
    name: str
    age: int
    team_id: int


class MemberCreate(MemberBase):
    pass


class MemberUpdate(MemberBase):
    pass


class Member(MemberBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    members: List[Member]

    class Config:
        orm_mode = True


class TeamStats(List[Team]):
    avg_age: float

    class Config:
        orm_mode = True
