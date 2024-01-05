from moex_alerter_bot.config import LOGGER

from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начало работы"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="stop", description="Окончание работы"),
        BotCommand(command="settings", description="Настройки"),
    ]
    result = await bot.set_my_commands(commands=commands)
    LOGGER.info(result)
