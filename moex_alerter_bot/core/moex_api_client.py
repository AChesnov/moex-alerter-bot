import datetime
from dataclasses import dataclass
from decimal import Decimal

import holidays
import httpx
from bs4 import BeautifulSoup, element

from moex_alerter_bot.config import LOGGER


@dataclass
class Stock:
    name: str
    short_name: str
    price: Decimal | None = None

    def __repr__(self):
        return f'Stock(name={self.name}, short_name={self.short_name}, price={self.price})'


class MoexApiClient:
    T2_RU_OPEN_PRE_MARKET_MORNING_TIME = datetime.time(9, 50, 0)
    T2_RU_CLOSE_POST_MARKET_MORNING_TIME = datetime.time(18, 40, 0)
    T2_RU_OPEN_PRE_MARKET_EVENING_TIME = datetime.time(19, 0, 1)
    T2_RU_CLOSE_POST_MARKET_EVENING_TIME = datetime.time(23, 49, 59)

    def __init__(self):
        self.url = 'https://iss.moex.com'
        self.board_id = 'TQBR'

    @classmethod
    def is_moex_work_time(cls) -> bool:
        """Проверяем, что текущее время совпадает со временем работы биржи"""
        dt = datetime.datetime.now()
        date = dt.date()
        time = dt.time()
        cls.is_work_day(current_date=date)
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

    def parse_row_from_text(self, text) -> list[dict[str, str]]:
        soup = BeautifulSoup(text, 'xml')
        rows: list[element.Tag] = soup.find_all('row')
        return [row.attrs for row in rows if row.attrs.get('BOARDID') == self.board_id]

    @staticmethod
    def parse_stocks_info(rows: list[dict[str, str]]) -> list[Stock] | None:
        """BOARDNAME = Т+: Неполные лоты (акции) - безадрес."""
        stocks = []
        for row in rows:
            price = row.get('LAST') or row.get('MARKETPRICE') or row.get('PREVPRICE')
            LOGGER.info(f'\n{row=}\n{price=}\n')
            if row.get('SHORTNAME') and price:
                stocks.append(
                    Stock(
                        name=row['SECID'],
                        short_name=row['SHORTNAME'],
                        price=round(Decimal(price), 2),
                    ),
                )
        return stocks

    async def send_request(self, path: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.url}{path}')
            return response.text

    async def get_tickers(self) -> list[Stock]:
        result = await self.send_request(path='/iss/engines/stock/markets/shares/securities.xml')
        rows = self.parse_row_from_text(text=result)
        stocks = self.parse_stocks_info(rows)
        return stocks

    async def get_ticker_info(self, ticker_name: str) -> Stock | None:
        """Возвращаем информацию по акции если она есть"""
        result = await self.send_request(path=f'/iss/engines/stock/markets/shares/securities/{ticker_name.upper()}.xml')
        rows = self.parse_row_from_text(text=result)
        stocks = self.parse_stocks_info(rows)
        if stocks:
            return stocks[0]
