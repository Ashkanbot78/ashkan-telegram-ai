import os
from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

BOT_USERNAME = "AshkanChatAI_bot"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    # در گروه فقط وقتی ربات منشن شده یا به پیام ربات Reply شده پاسخ بده
    chat_type = update.message.chat.type

    if chat_type in ["group", "supergroup"]:
        mentioned = f"@{BOT_USERNAME.lower()}" in text.lower()
        replied_to_bot = (
            update.message.reply_to_message is not None
            and update.message.reply_to_message.from_user is not None
            and update.message.reply_to_message.from_user.username
            and update.message.reply_to_message.from_user.username.lower()
            == BOT_USERNAME.lower()
        )

        if not mentioned and not replied_to_bot:
            return

        # حذف منشن ربات از متن سؤال
        text = text.replace(f"@{BOT_USERNAME}", "")
        text = text.replace(f"@{BOT_USERNAME.lower()}", "")
        text = text.strip()

    if not text:
        await update.message.reply_text("بله؟ 😊 سؤالت رو بپرس.")
        return

    try:
        response = await openai_client.responses.create(
            model="gpt-6-luna",
            instructions=(
                "تو دستیار هوش مصنوعی یک گروه تلگرامی هستی. "
                "به فارسی روان، دوستانه و مفید پاسخ بده. "
                "اگر کاربر فارسی صحبت کرد، فارسی جواب بده."
            ),
            input=text,
        )

        answer = response.output_text

        await update.message.reply_text(answer)

    except Exception as error:
        print("OpenAI error:", error)
        await update.message.reply_text(
            "متأسفم، فعلاً در ارتباط با هوش مصنوعی مشکلی پیش آمده 😕"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "من دستیار هوش مصنوعی گروه هستم.\n"
        "من را در گروه منشن کن و سؤالت را بپرس."
    )


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.COMMAND, start))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Ashkan AI Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
