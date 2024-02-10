import prettytable as pt
from aiogram import Bot

from moex_alerter_bot.config import LOGGER
from moex_alerter_bot.core import db
from moex_alerter_bot.core.moex_api_client import MoexApiClient


def format_text(values: dict) -> str:
    """
    'interest': Decimal(config.INTEREST_LEVELS.get(ticker)),
    'buy': Decimal(config.BUY_LEVELS.get(ticker)),
    'current_price': current_price
    """
    table = pt.PrettyTable(['ticker', 'current_price', 'interest', 'buy'])

    for ticker in values:
        table.add_row(
            [
                ticker,
                values[ticker].get('current_price'),
                values[ticker].get('interest'),
                values[ticker].get('buy'),
            ],
        )

    return str(table)


async def check_stocks_price(bot: Bot):
    moex_client = MoexApiClient()
    LOGGER.info(moex_client.is_moex_work_time())
    stocks = await db.get_stocks()
    stocks_info = []
    for stock in stocks:
        stocks_info.append(await moex_client.get_ticker_info(stock.name))
    LOGGER.info(stocks_info)

    # if not moex_client.is_moex_work_time():
    #     return
    # await bot.send_message(chat_id=CHAT_ID, text='Test message')


# def check_interest_levels() -> Optional[Dict]:
#     tickers = []
#
#     for ticker in tickers:
#         try:
#             ticker_summary = get_current_price_by_ticker(ticker=ticker)
#             if not ticker_summary:
#                 continue
#
#             if current_price := ticker_summary[0].get('LAST'):
#                 current_price = round(Decimal(current_price), 2)
#             else:
#                 current_price = round(Decimal(ticker_summary[0].get('MARKETPRICE')), 2)
#
#             interest_price = round(Decimal(config.INTEREST_LEVELS.get(ticker)), 2)
#             buy_price = round(Decimal(config.BUY_LEVELS.get(ticker)), 2)
#
#             if current_price < interest_price or current_price < buy_price:
#                 if current_price > buy_price and ticker in already_notified:
#                     continue
#                 already_notified.add(ticker)
#                 interest_levels[ticker] = {
#                     'interest': interest_price,
#                     'buy': buy_price,
#                     'current_price': current_price
#                 }
#         except Exception as err:
#             print(f'{ticker}: {err}')
#
#     return interest_levels
