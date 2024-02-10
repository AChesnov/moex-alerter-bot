from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from moex_alerter_bot.config import DB_URL
from moex_alerter_bot.models.stock import Stock

engine = create_async_engine(DB_URL, echo=True, future=True)
ASYNC_SESSION = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_stocks() -> list[Stock]:
    query = select(Stock)
    async with ASYNC_SESSION() as session:
        # sqlalchemy.engine.result.ChunkedIteratorResult
        qs = await session.execute(query)
        stocks = qs.scalars().fetchall()
        return stocks


async def add_stock(stock: Stock) -> None:
    async with ASYNC_SESSION() as session:
        # sqlalchemy.engine.result.ChunkedIteratorResult
        session: AsyncSession
        session.add(stock)
        await session.commit()
