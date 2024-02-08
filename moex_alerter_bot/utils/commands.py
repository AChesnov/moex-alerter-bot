from aiogram import Bot
from aiogram.types import BotCommand

from moex_alerter_bot.config import LOGGER


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Start bot'),
        BotCommand(command='help', description='Help'),
        BotCommand(command='stop', description='Stop bot'),
        BotCommand(command='settings', description='Settings'),
    ]
    result = await bot.set_my_commands(commands=commands)
    LOGGER.info('Set commands result: %s', result)
