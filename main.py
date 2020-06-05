from aiohttp import web
from db import close_pg, init_pg
import db
import sqlalchemy


async def handle(request):
    async with request.app['db'].acquire() as conn:
        # Создаем курсор и получаем все данные
        cursor = await conn.execute(db.user.select())
        # Показываем результат
        records = await cursor.fetchall()
        users = [dict(u) for u in records]
        return web.Response(text=str(users))


async def insert_user(request):
    user_id = 7
    async with request.app['db'].acquire() as conn:
        # Создаем курсор и получаем все данные
        ins = db.user.insert().values(id=user_id)
        cursor = await conn.execute(ins)


async def delete_user(request):
    async with request.app['db'].acquire() as conn:
        # Создаем курсор и получаем все данные
        ins = db.user.delete().where(db.user.c.id > 0)
        cursor = await conn.execute(ins)


async def show_user(request):
    # print(request)
    # user_id = request.rel_url.query['user_id']
    # print(dict(request.rel_url.query))
    # print(user_id)
    """  Returns json data about a single user  """
    async with request.app['db'].acquire() as conn:
        user_id = int(request.match_info.get('user_id'))
        ins = db.user.select().where(db.user.c.id == user_id)
        # print(str(ins))
        # print(ins.compile().params)
        cursor = await conn.execute(ins)  # выполнить
        records = await cursor.fetchall()
        users = [dict(u) for u in records]
        if len(users) == 0:
            return web.Response(text="{ error : \"User doesn't exist\" }")
        else:
            return web.Response(text=str(users))


async def edit_user(request):
    """  Edit user data  """
    async with request.app['db'].acquire() as conn:
        ins = db.user.select().where(db.user.c.id == 0)
        # print(str(ins))
        # print(ins.compile().params)
        cursor = await conn.execute(ins)  # выполнить
        records = await cursor.fetchall()
        users = [dict(u) for u in records]
        return web.Response(text=str(users))


async def search_user(request):
    """  Returns json data users after search  """
    return web.Response(text='Hello world!')


async def login(request):
    return web.Response(text='Hello world!')


app = web.Application()  #
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
app.add_routes([web.get('/', handle),
                web.post('/login/', login),
                web.get('/users/{user_id}/', show_user),
                web.post('/users/', edit_user),
                web.post('/add_user/', insert_user),
                web.post('/delete_user/', delete_user),
                ])

if __name__ == '__main__':
    web.run_app(app)
