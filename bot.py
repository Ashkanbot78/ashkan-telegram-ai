import os
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# تشخیص لینک
LINK_PATTERN = re.compile(
    r"(https?://\S+|www\.\S+|t\.me/\S+|telegram\.me/\S+)",
    re.IGNORECASE
)


async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    # فقط در گروه‌ها
    if update.message.chat.type not in ["group", "supergroup"]:
        return

    text = update.message.text

    # اگر لینک داشت، پیام را حذف کن
    if LINK_PATTERN.search(text):
        try:
            await update.message.delete()
        except Exception as error:
            print("Delete error:", error)


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            anti_link
        )
    )

    print("Ashkan Anti-Link Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
