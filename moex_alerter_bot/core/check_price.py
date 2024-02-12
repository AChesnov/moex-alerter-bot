import prettytable as pt
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

from moex_alerter_bot.config import CHAT_ID
from moex_alerter_bot.core import db
from moex_alerter_bot.core.moex_api_client import MoexApiClient, StockInfo


def format_text(stocks_info: dict[db.StockAnalyze, StockInfo]) -> str:
    """Создаем табличку со значениями по интересным уровням"""
    table = pt.PrettyTable(['ticker', 'price', 'top', 'bottom'])
    for stock_analyze, stock_info in stocks_info.items():
        table.add_row([stock_info.name, stock_info.price, stock_analyze.top_limit, stock_analyze.bottom_limit])
    return f'```{table}```'


def filter_price_levels(stocks_info: dict[db.StockAnalyze, StockInfo]) -> dict[db.StockAnalyze, StockInfo]:
    """Фильтруем price по уровням, по которым мониторим акцию"""
    filtered_stocks_info: dict[db.StockAnalyze, StockInfo] = {}
    for stock_analyze, stock_info in stocks_info.items():
        if stock_info.price > stock_analyze.top_limit or stock_info.price < stock_analyze.bottom_limit:
            filtered_stocks_info[stock_analyze] = stock_info
    return filtered_stocks_info


async def fetch_stocks_info() -> dict[db.StockAnalyze, StockInfo]:
    """Забираем параметры мониторинга и ходим по всем ticker-ам и забираем stock_info"""
    stocks_info = {}
    moex_client = MoexApiClient()
    if not moex_client.is_moex_work_time():
        return stocks_info

    stocks_analyze = await db.get_stocks_analyze()
    for stock_analyze in stocks_analyze:
        stocks_info[stock_analyze] = await moex_client.get_stock_info(stock_name=stock_analyze.stock.name)
    return stocks_info


async def check_stocks_price(bot: Bot):
    stocks_info = await fetch_stocks_info()
    stocks_info = filter_price_levels(stocks_info=stocks_info)

    if stocks_info:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=format_text(stocks_info=stocks_info),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
