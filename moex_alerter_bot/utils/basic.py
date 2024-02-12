from aiogram import Bot, Dispatcher
from aiohttp.web import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from moex_alerter_bot.config import LOGGER, WEBHOOK_URL
from moex_alerter_bot.core.check_price import check_stocks_price
from moex_alerter_bot.routes import register_routes
from moex_alerter_bot.utils.commands import set_commands


async def set_web_hook(bot: Bot) -> None:
    webhook_info = await bot.get_webhook_info()
    LOGGER.info('Current webhook %s', webhook_info)
    if webhook_info.url != WEBHOOK_URL:
        LOGGER.info('Set new webhook %s', WEBHOOK_URL)
        result = await bot.set_webhook(url=WEBHOOK_URL)
        LOGGER.info('Set webhook status: %s', result)


async def start_scheduler(bot: Bot) -> None:
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(func=check_stocks_price, trigger='interval', minutes=1, kwargs={'bot': bot})
    scheduler.start()


async def on_startup(dispatcher: Dispatcher, bot: Bot, app: Application) -> None:
    """Обработчик запуска приложения, засылает webhook в телеграм"""
    await set_web_hook(bot=bot)

    LOGGER.info('Register routes')
    register_routes(dispatcher=dispatcher)

    LOGGER.info('Set bot commands')
    await set_commands(bot=bot)

    LOGGER.info('Start scheduler')
    await start_scheduler(bot=bot)


async def on_shutdown(bot: Bot) -> None:
    LOGGER.info('Starting of graceful shutdown')
    await bot.delete_webhook()
    await bot.session.close()
    LOGGER.info('Finish of graceful shutdown')
