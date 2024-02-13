import prettytable as pt
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

from moex_alerter_bot.config import CHAT_ID
from moex_alerter_bot.core import db
from moex_alerter_bot.core.moex_api_client import MoexApiClient, StockPrice


def format_text(stock_prices: dict[db.StockAnalyze, StockPrice]) -> str:
    """Создаем табличку со значениями по интересным уровням"""
    table = pt.PrettyTable(['ticker', 'price', 'top', 'bottom'])
    for stock_analyze, stock_price in stock_prices.items():
        table.add_row([stock_price.name, stock_price.price, stock_analyze.top_limit, stock_analyze.bottom_limit])
    return f'```{table}```'


def filter_price_levels(stock_prices: dict[db.StockAnalyze, StockPrice]) -> dict[db.StockAnalyze, StockPrice]:
    """Фильтруем price по уровням, по которым мониторим акцию"""
    filtered_stocks_info: dict[db.StockAnalyze, StockPrice] = {}
    for stock_analyze, stock_price in stock_prices.items():
        if stock_price.price > stock_analyze.top_limit or stock_price.price < stock_analyze.bottom_limit:
            filtered_stocks_info[stock_analyze] = stock_price
    return filtered_stocks_info


async def fetch_stock_prices() -> dict[db.StockAnalyze, StockPrice]:
    """Забираем параметры мониторинга и ходим по всем ticker-ам и забираем stock_info"""
    stock_prices = {}
    moex_client = MoexApiClient()
    if not moex_client.is_moex_work_time():
        return stock_prices

    stocks_analyze = await db.get_stocks_analyze()
    for stock_analyze in stocks_analyze:
        stock_prices[stock_analyze] = await moex_client.get_stock_price(stock_name=stock_analyze.stock.name)
    return stock_prices


async def check_stocks_price(bot: Bot):
    stock_prices = await fetch_stock_prices()
    stock_prices = filter_price_levels(stock_prices=stock_prices)

    if stock_prices:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=format_text(stock_prices=stock_prices),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
