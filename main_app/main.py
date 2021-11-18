from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .dals.member_dal import MemberDAL
from .dals.team_dal import TeamDAL
from . import schemas
from .dependencies import get_member_dal, get_team_dal

app = FastAPI()


@app.post("/create_player/", response_model=schemas.Member)
async def create_member(
    member: schemas.MemberCreate, member_dal: MemberDAL = Depends(get_member_dal)
):
    return await member_dal.create_member(member=member, team_id=member.team_id)


@app.get("/player/{player_id}", response_model=schemas.Member)
async def read_member(player_id: int, member_dal: MemberDAL = Depends(get_member_dal)):
    member = await member_dal.read_member(player_id=player_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@app.put("/player/{player_id}", response_model=schemas.Member)
async def update_member(
    player_id: int,
    member: schemas.MemberUpdate,
    member_dal: MemberDAL = Depends(get_member_dal),
):
    member_in_db = await member_dal.read_member(player_id=player_id)
    if not member_in_db:
        raise HTTPException(status_code=404, detail="Member not found")
    return await member_dal.update_member(player_id=player_id, member=member)


@app.delete("/player/{player_id}", response_model=schemas.Member)
async def delete_member(
    player_id: int, member_dal: MemberDAL = Depends(get_member_dal)
):
    member_in_db = await member_dal.read_member(player_id=player_id)
    if not member_in_db:
        raise HTTPException(status_code=404, detail="Member not found")

    await member_dal.delete_member(player_id=player_id)
    return JSONResponse(status_code=204, content={"message": "Member deleted"})


@app.get("/teams/", response_model=List[schemas.Team])
async def read_teams(team_dal: TeamDAL = Depends(get_team_dal)):
    return await team_dal.read_teams()


@app.get("/teams/average_age", response_model=List[schemas.TeamStats])
async def read_teams_by_average_age(
    order: str = "asc", team_dal: TeamDAL = Depends(get_team_dal)
):
    return await team_dal.read_team_members_average_age(order)
