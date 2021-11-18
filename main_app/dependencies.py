from .database import async_session
from .dals.member_dal import MemberDAL
from .dals.team_dal import TeamDAL


async def get_team_dal():
    async with async_session() as session:
        async with session.begin():
            yield TeamDAL(session)


async def get_member_dal():
    async with async_session() as session:
        async with session.begin():
            yield MemberDAL(session)
