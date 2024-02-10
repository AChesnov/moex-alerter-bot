from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup, element


@dataclass
class Stock:
    name: str
    short_name: str

    def __repr__(self):
        return f'Stock(name={self.name}, short_name={self.short_name})'


class MoexApiClient:
    def __init__(self):
        self.url = 'https://iss.moex.com'
        self.board_id = 'TQBR'

    async def send_request(self, path: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.url}{path}')
            return response.text

    def parse_row_from_text(self, text) -> list[dict[str, str]]:
        soup = BeautifulSoup(text, 'xml')
        rows: list[element.Tag] = soup.find_all('row')
        return [row.attrs for row in rows if row.attrs.get('BOARDID') == self.board_id]

    @staticmethod
    def parse_stock_tickers(rows: list[dict[str, str]]) -> list[Stock] | None:
        return [Stock(name=row['SECID'], short_name=row['SHORTNAME']) for row in rows if row.get('SHORTNAME')]

    async def get_tickers(self) -> list[Stock]:
        result = await self.send_request(path='/iss/engines/stock/markets/shares/securities.xml')
        rows = self.parse_row_from_text(text=result)
        stocks = self.parse_stock_tickers(rows)
        return stocks

    async def get_ticker(self, ticker_name: str) -> Stock | None:
        """Возвращаем информацию по акции если она есть"""
        result = await self.send_request(path=f'/iss/engines/stock/markets/shares/securities/{ticker_name.upper()}.xml')
        rows = self.parse_row_from_text(text=result)
        stocks = self.parse_stock_tickers(rows)
        if stocks:
            return stocks[0]
