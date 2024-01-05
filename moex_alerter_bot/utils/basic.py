from moex_alerter_bot.config import LOGGER, WEBHOOK_URL
from moex_alerter_bot.routes import register_routes
from moex_alerter_bot.utils.commands import set_commands

from aiogram import Dispatcher, Bot


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    """Обработчик запуска приложения, засылает webhook в телеграм"""
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        LOGGER.info("Set webhook %s", webhook_info)
        await bot.set_webhook(url=WEBHOOK_URL)

    LOGGER.info("Register routes")
    register_routes(dispatcher=dispatcher)

    LOGGER.info("Set bot commands")
    await set_commands(bot=bot)


async def on_shutdown(bot: Bot):
    LOGGER.info('Starting of graceful shutdown')
    await bot.delete_webhook()
    await bot.session.close()
    LOGGER.info('Finish of graceful shutdown')
