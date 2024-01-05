from moex_alerter_bot.config import WEBHOOK_PATH, BOT_TOKEN
from moex_alerter_bot.utils.basic import on_shutdown, on_startup

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web


def run():
    # Dispatcher is a root router
    dp = Dispatcher()

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

    # Register startup/shutdown logic
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)

    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host='0.0.0.0', port=8081)
