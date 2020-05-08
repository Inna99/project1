from aiohttp import web
from db import close_pg, init_pg
import db


async def handle(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.user.select())
        records = await cursor.fetchall()
        users = [dict(u) for u in records]
        return web.Response(text=str(users))

app = web.Application()
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app)
