import asyncio
from telegram import Bot

BOT_TOKEN = "8451147108:AAG8TRY1NodP0k5uvy6WYYlyU1nNf4ZnHcU"

USERNAMES = [
    "@BK9Aus"
]

async def main():
    bot = Bot(BOT_TOKEN)
    chat = await bot.get_chat("@BK9Aus")
    print(chat.id)

if __name__ == "__main__":
    asyncio.run(main())
