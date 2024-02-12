import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar, Mapping
from urllib.parse import urljoin

import holidays
import httpx
from bs4 import BeautifulSoup, element

from moex_alerter_bot.config import MOEX_BOARD_ID, MOEX_BOARD_NAME, MOEX_ENGINES, MOEX_MARKETS


@dataclass
class StockInfo:
    name: str
    short_name: str
    price: Decimal | None = None

    def __repr__(self):
        return f'StockInfo(name={self.name}, short_name={self.short_name}, price={self.price})'


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

    def parse_row_from_text(self, text) -> list[Mapping[str, str]]:
        soup = BeautifulSoup(text, 'xml')
        rows: list[element.Tag] = soup.find_all('row')
        return [
            row.attrs
            for row in rows
            if row.attrs.get('BOARDID') == self.board_id and row.attrs.get('BOARDNAME') == self.board_name
        ]

    @staticmethod
    def parse_stocks_info(rows: list[Mapping[str, str]]) -> list[StockInfo] | None:
        stocks = []
        for row in rows:
            price = row.get('LAST') or row.get('MARKETPRICE') or row.get('PREVPRICE')
            if row.get('SHORTNAME') and price:
                stocks.append(
                    StockInfo(name=row['SECID'], short_name=row['SHORTNAME'], price=round(Decimal(price), 2)),
                )
        return stocks

    async def send_request(self, path: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(urljoin(self.url, path))
            return response.text

    async def get_tickers(self) -> list[StockInfo]:
        """Возвращаем информацию по акциям"""
        path = f'/iss/engines/{self.engines}/markets/{self.markets}/securities.xml'
        result = await self.send_request(path=path)
        rows = self.parse_row_from_text(text=result)
        stocks = self.parse_stocks_info(rows)
        return stocks

    async def get_stock_info(self, stock_name: str) -> StockInfo | None:
        """Возвращаем информацию по акции если она есть"""
        path = f'/iss/engines/{self.engines}/markets/{self.markets}/securities/{stock_name.upper()}.xml'
        result = await self.send_request(path=path)
        rows = self.parse_row_from_text(text=result)
        stocks = self.parse_stocks_info(rows)
        if stocks:
            return stocks[0]
