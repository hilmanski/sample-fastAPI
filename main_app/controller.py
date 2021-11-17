from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from . import models, schemas

def create_member(db: Session, member: schemas.MemberCreate, team_id: int):
    db_member = models.Member(name=member.name, age=member.age, team_id=team_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def read_member(db: Session, player_id: int):
    return db.query(models.Member).filter(models.Member.id == player_id).first()

def update_member(db: Session, member: schemas.MemberUpdate, player_id: int):
    db_member = read_member(db, player_id)
    if db_member is None:
        raise Exception("Member not found")
    db_member.name = member.name
    db_member.age = member.age
    db_member.team_id = member.team_id
    db.commit()
    return db_member

def delete_member(db: Session, player_id: int):
    db_member = read_member(db, player_id)
    if db_member is None:
        raise Exception("Member not found")
    db.delete(db_member)
    db.commit()
    return db_member


def read_teams(db: Session):
    return db.query(models.Team).all()

def read_teams_sorted(db: Session):
    return db.query(models.Team).join(models.Team.members).\
                    group_by(models.Team.id).order_by(func.avg(models.Member.age)).all()


def read_teams_sorted_desc(db: Session):
    return db.query(models.Team).join(models.Team.members).\
            group_by(models.Team.id).order_by(func.avg(models.Member.age).desc()).all()
