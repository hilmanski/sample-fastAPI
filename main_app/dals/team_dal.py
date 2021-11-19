from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from main_app import models
from sqlalchemy.future import select
from sqlalchemy.sql import func
from sqlalchemy import text


class TeamDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def read_teams(self):
        query = await self.db_session.execute(select(models.Team))
        return query.scalars().all()

    async def read_team_members_average_age(self, order):

        query = await self.db_session.execute(
            select(
                models.Team.id.label("id"),
                models.Team.name.label("name"),
                func.avg(models.Member.age).label("average_age"),
            )
            .join(models.Team.members)
            .group_by(models.Team.id)
            .order_by(func.avg(models.Member.age))
        )
        results = query.all()

        if order == "desc":
            results.reverse()
            return results

        return results
