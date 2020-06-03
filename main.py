from aiohttp import web
from db import close_pg, init_pg
import db
import sqlalchemy


class SQLUser:
    async def handle(self, request):
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

    async def delete_user(self, request):
        async with request.app['db'].acquire() as conn:
            # Создаем курсор и получаем все данные
            ins = db.user.delete().where(db.user.c.id > 0)
            cursor = await conn.execute(ins)

    async def show_user(self, request):
        """  Returns json data about a single user  """
        async with request.app['db'].acquire() as conn:
            ins = db.user.select().where(db.user.c.id > 0)
            # print(str(ins))
            # print(ins.compile().params)
            cursor = await conn.execute(ins)  # выполнить
            records = await cursor.fetchall()
            users = [dict(u) for u in records]
            return web.Response(text=str(users))

    async def edit_user(self, request):
        """  Edit user data  """
        async with request.app['db'].acquire() as conn:
            ins = db.user.select().where(db.user.c.id > 0)
            # print(str(ins))
            # print(ins.compile().params)
            cursor = await conn.execute(ins)  # выполнить
            records = await cursor.fetchall()
            users = [dict(u) for u in records]
            return web.Response(text=str(users))

    async def search_user(self, request):
        """  Returns json data users after search  """
        return web.Response(text='Hello world!')

    async def login(self, request):
        return web.Response(text='Hello world!')


sql_user = SQLUser()

app = web.Application()  #
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
app.add_routes([web.get('/', SQLUser.handle),
                web.post('/login/', sql_user.login),
                web.get('/users/{}/'.format(1), sql_user.show_user),
                web.post('/users/{}/'.format(1), sql_user.edit_user),
                web.get('/users/', sql_user.search_user),
                web.post('/add_user/', sql_user.insert_user),
                web.post('/delete_user/', sql_user.delete_user),
                ])

if __name__ == '__main__':
    web.run_app(app)
