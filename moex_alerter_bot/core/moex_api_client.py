import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, ClassVar
from urllib.parse import urljoin

import holidays
import httpx

from moex_alerter_bot.config import MOEX_BOARD_ID, MOEX_BOARD_NAME, MOEX_ENGINES, MOEX_MARKETS

"""
SECID - Идентификатор финансового инструмента
BOARDID - Идентификатор режима торгов
OPEN - Цена первой сделки
LOW - Минимальная цена сделки
HIGH - Максимальная цена сделки
LAST - Цена последней сделки

LCURRENTPRICE - Официальная текущая цена, средневзвешенная цена сделок заключенных за последние 10 минут
LAST - Цена последней сделки

"""


@dataclass
class SecuritiesResponseData:
    securities: list[dict[str, Any]]
    marketdata: list[dict[str, Any]]


@dataclass
class StockInfo:
    name: str
    short_name: str

    def __repr__(self):
        return f'StockInfo(name={self.name}, short_name={self.short_name})'


@dataclass
class StockPrice:
    name: str
    price: Decimal

    def __repr__(self):
        return f'StockPrice(name={self.name}, price={self.price})'


@dataclass
class MoexApiClient:
    T2_RU_OPEN_PRE_MARKET_MORNING_TIME: ClassVar[datetime.time] = datetime.time(9, 50, 0)
    T2_RU_CLOSE_POST_MARKET_MORNING_TIME: ClassVar[datetime.time] = datetime.time(18, 40, 0)
    T2_RU_OPEN_PRE_MARKET_EVENING_TIME: ClassVar[datetime.time] = datetime.time(19, 0, 1)
    T2_RU_CLOSE_POST_MARKET_EVENING_TIME: ClassVar[datetime.time] = datetime.time(23, 49, 59)

    url: str = 'https://iss.moex.com'
    board_name: str = MOEX_BOARD_NAME
    engines: str = MOEX_ENGINES
    board_id: str = MOEX_BOARD_ID
    markets: str = MOEX_MARKETS

    @classmethod
    def is_moex_work_time(cls) -> bool:
        """Проверяем, что текущее время совпадает со временем работы биржи"""
        current_datetime = datetime.datetime.now()
        date = current_datetime.date()
        time = current_datetime.time()
        return cls.is_work_day(current_date=date) and cls.is_work_time(current_time=time)

    @classmethod
    def is_work_time(cls, current_time: datetime.time):
        return cls.T2_RU_OPEN_PRE_MARKET_MORNING_TIME < current_time < cls.T2_RU_CLOSE_POST_MARKET_MORNING_TIME

    @staticmethod
    def is_work_day(current_date: datetime.date) -> bool:
        ru = holidays.RU()
        if current_date in ru:
            return False
        if current_date.isoweekday() in (6, 7):
            return False
        return True

    @staticmethod
    def convert_response(json_response: dict) -> SecuritiesResponseData:
        return SecuritiesResponseData(
            securities=[
                dict(zip(json_response.get('securities').get('columns'), row))
                for row in json_response.get('securities').get('data')
            ],
            marketdata=[
                dict(zip(json_response.get('marketdata').get('columns'), row))
                for row in json_response.get('marketdata').get('data')
            ],
        )

    def _get_stock_info(self, securities: SecuritiesResponseData) -> StockInfo | None:
        for row in securities.securities:
            if row.get('BOARDID') == self.board_id:
                return StockInfo(name=row['SECID'], short_name=row['SHORTNAME'])

    def _get_stock_price(self, securities: SecuritiesResponseData) -> StockPrice | None:
        for row in securities.marketdata:
            stock_current_price = row.get('LAST') or row.get('LCURRENTPRICE')
            if row.get('BOARDID') == self.board_id and stock_current_price:
                return StockPrice(name=row['SECID'], price=round(Decimal(stock_current_price), 2))

    async def send_request(self, path: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(urljoin(self.url, path))
            return response.json()

    async def get_stock_info(self, stock_name: str) -> StockInfo | None:
        """Возвращаем информацию по акции если она есть"""
        path = f'/iss/engines/{self.engines}/markets/{self.markets}/securities/{stock_name.upper()}.json'
        response = await self.send_request(path=path)
        securities_response = self.convert_response(json_response=response)
        return self._get_stock_info(securities=securities_response)

    async def get_stock_price(self, stock_name: str) -> StockPrice | None:
        """Возвращаем информацию по акции если она есть"""
        path = f'/iss/engines/{self.engines}/markets/{self.markets}/securities/{stock_name.upper()}.json'
        response = await self.send_request(path=path)
        securities_response = self.convert_response(json_response=response)
        return self._get_stock_price(securities=securities_response)
