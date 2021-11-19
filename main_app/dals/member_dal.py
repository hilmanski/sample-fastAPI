from sqlalchemy.orm import Session
from main_app import models, schemas
from sqlalchemy import update, delete
from sqlalchemy.future import select


class MemberDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_member(self, member: schemas.MemberCreate, team_id: int):
        new_member = models.Member(name=member.name, age=member.age, team_id=team_id)
        self.db_session.add(new_member)
        await self.db_session.commit()

    async def read_member(self, player_id: int):
        query = await self.db_session.execute(
            select(models.Member).filter(models.Member.id == player_id)
        )
        return query.scalars().first()

    async def update_member(self, member: schemas.MemberUpdate, player_id: int):
        query = update(models.Member).where(models.Member.id == player_id)
        query = query.values(name=member.name, age=member.age, team_id=member.team_id)
        await self.db_session.execute(query)

    async def delete_member(self, player_id: int):
        query = delete(models.Member).where(models.Member.id == player_id)
        await self.db_session.execute(query)
