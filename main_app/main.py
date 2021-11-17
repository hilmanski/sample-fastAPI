from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import controller, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_player/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    return controller.create_member(db=db, member=member, team_id=member.team_id)

@app.get("/player/{player_id}", response_model=schemas.Member)
def read_member(player_id: int, db: Session = Depends(get_db)):
    member = controller.read_member(db=db, player_id=player_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@app.put("/player/{player_id}", response_model=schemas.Member)
def update_member(player_id: int, member: schemas.MemberUpdate, db: Session = Depends(get_db)):
    member_in_db = controller.read_member(db=db, player_id=player_id)
    if not member_in_db:
        raise HTTPException(status_code=404, detail="Member not found")
    return controller.update_member(db=db, player_id=player_id, member=member)

@app.delete("/player/{player_id}", response_model=schemas.Member)
def delete_member(player_id: int, db: Session = Depends(get_db)):
    member = controller.read_member(db=db, player_id=player_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    controller.delete_member(db=db, player_id=player_id)
    return JSONResponse(status_code=204, content={"message": "Member deleted"})

@app.get("/teams/", response_model=List[schemas.Team])
def read_teams(db: Session = Depends(get_db)):
    teams = controller.read_teams(db)
    return teams

@app.get("/teams/average_age", response_model=List[schemas.Team])
def read_teams_by_average_age(db: Session = Depends(get_db)):
    teams = controller.read_teams_sorted(db)
    return teams


@app.get("/teams/average_age_desc", response_model=List[schemas.Team])
def read_teams_by_average_age(db: Session = Depends(get_db)):
    teams = controller.read_teams_sorted_desc(db)
    return teams
