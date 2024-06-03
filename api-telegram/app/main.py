from typing import Union
from fastapi import FastAPI

import asyncio
from telegram import Bot

import json

from loguru import logger

import os

env = os.environ.get("ENV", "prod")
env_token = os.environ.get("TOKEN", None)
env_users_file = os.environ.get("USERS_FILE", "/users/users.json")


def env_validations() -> None:
    logger.debug(f"env: {env}")
    
    if env not in ['prod', 'dev']:
        logger.error("Invalid ENV provided. env not set.")
        exit(1)

    if env_token is None:
        logger.error("Invalid TOKEN provided. TOKEN not set.")
        exit(1)
    
    if env_users_file is None:
        logger.error("Invalid USERS_FILE provided. USERS_FILE not set.")
        exit(1)


def loguro_config() -> None:
    if env == 'prod':
        logger.add("./log/{time:YYYY-MM-DD}.log", rotation="250 MB", level="WARNING")
    else:
        logger.add("./log/{time:YYYY-MM-DD}.log", rotation="250 MB", level="DEBUG")
    # logger.debug("This is a debug message")
    # logger.info("This is an info message")
    # logger.success("This is a success message")
    # logger.warning("This is a warning message")
    # logger.error("This is an error message")


loguro_config()
env_validations()

if env == 'prod':
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "up"}


@app.get("/msg")
def msg(msg: Union[str]):
    # read from file
    with open(env_users_file, 'r') as f:
        users = json.load(f)

    for user in users:
        asyncio.run(send_operando(user["id"], msg))

    return {"msg": "ok"}


async def send_operando(CHAT_ID, msg) -> None:
    bot = Bot(token=env_token)
    await bot.send_message(chat_id=CHAT_ID, text=msg)


def main(users:list) -> None:
    for i in users:
        asyncio.run(send_operando())
    