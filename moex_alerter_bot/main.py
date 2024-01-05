from moex_alerter_bot.config import BOT, DP, LOGGER, WEBHOOK_PATH
from moex_alerter_bot.utils.basic import lifespan

import uvicorn
from fastapi import FastAPI
from aiogram import types


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def webhook_handler(update: types.Update):
    LOGGER.info(update)
    await DP.feed_update(bot=BOT, update=update)


if __name__ == "__main__":
    uvicorn.run(app, port=8081, host="0.0.0.0")
