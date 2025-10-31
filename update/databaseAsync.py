from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker


class BaseDB:
    def __init__(self, async_engine):
        self.async_engine = async_engine
        self.AsyncSession = sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def dataGet(self, model, filters=None, custom_filters=None, order=None):
        # Открываем асинхронную сессию
        async with self.AsyncSession() as session:
            # Собираем запрос
            query = select(model)

            if filters:
                query = query.filter_by(**filters)
            if custom_filters:
                query = query.filter(*custom_filters)
            if order:
                query = query.order_by(*order)

            # Выполняем запрос
            result = await session.execute(query)
            return result.scalars().all()  # или .fetchall() для кортежей