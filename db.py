import aiopg.sa

from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String,
)

meta = MetaData()

user = Table(
    'user', meta,
    Column('id', Integer, primary_key=True),
    Column('username', String(200), nullable=False),
)


async def init_pg(app):
    # создание объекта указывающий на бд
    engine = await aiopg.sa.create_engine(
        database='postgres',
        user='postgres',
        password='docker',
        host='localhost',
        port='5432',
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
