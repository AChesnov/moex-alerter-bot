from typing import Type

from sqlalchemy import delete, select
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from moex_alerter_bot.config import DB_URL, LOGGER
from moex_alerter_bot.models.stock import Stock, StockAnalyze

engine = create_async_engine(DB_URL, echo=True, future=True)
ASYNC_SESSION = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def add_object(object_type: Stock | StockAnalyze) -> None:
    async with ASYNC_SESSION() as session:
        session: AsyncSession
        session.add(object_type)
        await session.commit()


async def delete_object(object_type: Type[Stock] | Type[StockAnalyze], object_id: int) -> None:
    query = delete(object_type).where(object_type.stock_id == object_id)
    LOGGER.debug(query)
    async with ASYNC_SESSION() as session:
        await session.execute(query)
        await session.commit()


async def get_stocks() -> list[Stock]:
    query = select(Stock)
    LOGGER.debug(query)
    async with ASYNC_SESSION() as session:
        result: ChunkedIteratorResult = await session.execute(query)
        return list(result.scalars().fetchall())


async def get_stock(stock_name: str) -> Stock | None:
    query = select(Stock).filter(Stock.name == stock_name)
    LOGGER.debug(query)
    async with ASYNC_SESSION() as session:
        result: ChunkedIteratorResult = await session.execute(query)
        return result.scalars().first()


async def get_stock_analyze(stock_id: int) -> Stock | None:
    query = select(StockAnalyze).filter(StockAnalyze.stock_id == stock_id)
    LOGGER.debug(query)
    async with ASYNC_SESSION() as session:
        result: ChunkedIteratorResult = await session.execute(query)
        return result.scalars().first()
