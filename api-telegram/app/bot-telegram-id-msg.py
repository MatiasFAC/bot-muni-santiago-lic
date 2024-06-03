import asyncio
from telegram import Bot

TOKEN = 'TOKEN'
CHAT_ID = 1231231232


async def send_operando():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="operando")


def main(users:list) -> None:
    for i in users:
        asyncio.run(send_operando())


if __name__ == '__main__':
    asyncio.run(send_operando())