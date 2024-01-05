from moex_alerter_bot.config import BOT, LOGGER, WEBHOOK_URL
from moex_alerter_bot.routes import register_routes
from moex_alerter_bot.utils.commands import set_commands

from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield
    await on_shutdown()


async def on_startup():
    """Обработчик запуска приложения, засылает webhook в телеграм"""
    webhook_info = await BOT.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        LOGGER.info("Set webhook %s", webhook_info)
        await BOT.set_webhook(url=WEBHOOK_URL)

    LOGGER.info("Register routes")
    register_routes()

    LOGGER.info("Set bot commands")
    await set_commands(bot=BOT)


async def on_shutdown():
    BOT.session.close()
