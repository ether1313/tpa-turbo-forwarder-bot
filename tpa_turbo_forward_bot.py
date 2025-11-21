import asyncio
import logging
import os
from telegram import Update
from logging.handlers import RotatingFileHandler
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# BOT TOKEN from Environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is missing.")

# Source Channel (TPA Main Group)
SOURCE_CHANNEL_ID = -1002595754142 #@tpaaustralia; 🇦🇺Trusted Pokies Australia🇦🇺 

# 10 Target Channels
TARGET_CHANNEL_IDS = [
    -1002662372702, #@rainbow13aus; 🇦🇺Australia Online Casino🇦🇺 
    -1002544806787, #@lvspin13aus; 🇦🇺 Online Gaming 🇦🇺
    -1002482016247, #@mario9aus; 🇦🇺BNG Australia Hot Game🇦🇺
    -1002194080801, #@jackpotaus; 🇦🇺 Australia Jackpot Online Casino🇦🇺
    -1002254333982, #@ZOMBIES9au; 🇦🇺Australia Jackpot Bonus🇦🇺
    -1002942441427, #@winpokies88; 🇦🇺Win Pokies AUstralia🇦🇺
    -1002444944113, #@plants9aus; 🇦🇺Pokies Australia Online Casino🇦🇺
    -1002748481631, #@rainbow1338; 🇦🇺Free Bonus 🇦🇺
    -1002226126447, #@Australiahotbng; 🇦🇺Sex Sex Girl Girl🇦🇺
    -1002284018291, #@hotgamtips; 🔞Sex Girl Australia 🔞
    -1002033860396, #@BK9Aus; 🇻🇬BK9 Australia Online Casino🇰🇾
]

# 防重复
processed_messages = set()

# Logging
os.makedirs("logs", exist_ok=True)

log_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=7,
    encoding="utf-8"
)

formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
log_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[log_handler, logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Auto Retry Forward (forward_message)
async def try_forward(bot, target, source, msg_id, max_retry=3):
    for attempt in range(1, max_retry + 1):
        try:
            await bot.forward_message(
                chat_id=target,
                from_chat_id=source,
                message_id=msg_id
            )
            logger.info(f"[SUCCESS] Forwarded to {target}")
            return True
        except Exception as e:
            logger.error(f"[ERROR] Attempt {attempt}/{max_retry} failed for {target}: {e}")

            if attempt < max_retry:
                await asyncio.sleep(2)

    return False

# Main Forward Logic
async def turbo_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.channel_post and update.channel_post.chat_id == SOURCE_CHANNEL_ID:
        msg_id = update.channel_post.message_id

        if msg_id in processed_messages:
            logger.info(f"[SKIP] Message {msg_id} already processed")
            return

        processed_messages.add(msg_id)

        logger.info(f"[INFO] New message detected (msg_id={msg_id}), forwarding...")

        for target in TARGET_CHANNEL_IDS:
            await try_forward(context.bot, target, SOURCE_CHANNEL_ID, msg_id)

# Fly.io Safe Start (no asyncio.run)
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.Chat(SOURCE_CHANNEL_ID) & filters.ALL,
            turbo_forward
        )
    )

    logger.info("🚀 TPA Turbo Forwarder is running and listening...")

    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
