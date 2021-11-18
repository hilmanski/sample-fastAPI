from sqlalchemy.orm import Session, lazyload, subqueryload
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

        rawQuery = text(
            """
            SELECT team.id as id, team.name as name, avg(member.age) as average_age
            FROM team
            LEFT JOIN member ON team.id = member.team_id
            GROUP BY team.id
            ORDER BY average_age
        """
        )

        query = await self.db_session.execute(rawQuery)
        results = query.all()

        if order == "desc":
            results.reverse()
            return results

        return results
