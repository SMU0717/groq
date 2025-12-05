from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

# API kalitlaringiz
TELEGRAM_TOKEN = "8597792902:AAFz1xfOjJIjvBToDobmZVuShfy-8UGRcfA"  # @BotFather dan
GROQ_API_KEY = "moonshotai/kimi-k2-instruct-0905"  # console.groq.com dan olingan haqiqiy API kalit

# Groq clientini yaratish
client = Groq(api_key=GROQ_API_KEY)


def query_ai(user_message):
    """Groq API bilan chat"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Siz foydali yordamchi AI assistentsiz. Qisqa va aniq javob bering."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="",  # To'g'ri model nomi
            temperature=0.7,
            max_tokens=300,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"❌ Xatolik: {str(e)}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot boshlash"""
    welcome = (
        "👋 Assalomu alaykum!\n\n"
        "🤖 Men AI botman\n"
        "💬 Menga savol bering!\n\n"
        "⚡️ Model: Qwen 2.5 32B\n"
        "🆓 Bepul\n"
        "⚡️ Juda tez"
    )
    await update.message.reply_text(welcome)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xabarga javob"""
    user_message = update.message.text

    if not user_message.strip():
        await update.message.reply_text("Iltimos, xabar kiriting!")
        return

    # Typing ko'rsatish
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    # AI javob olish (sync funksiyani async qilish)
    bot_reply = await asyncio.get_event_loop().run_in_executor(
        None, query_ai, user_message
    )

    # Yuborish
    await update.message.reply_text(bot_reply)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam"""
    help_text = (
        "📚 Bot haqida:\n\n"
        "🤖 Model: Qwen 2.5 (32B)\n"
        "🚀 API: Groq (eng tez!)\n"
        "💬 Menga istalgan savol bering!\n\n"
        "⚙️ Buyruqlar:\n"
        "/start - Boshlash\n"
        "/help - Yordam"
    )
    await update.message.reply_text(help_text)


def main():
    """Ishga tushirish"""
    print("🤖 Bot ishga tushmoqda...")

    try:
        app = Application.builder().token(TELEGRAM_TOKEN).build()

        # Handlerlar
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        print("✅ Bot ishlayapti! Ctrl+C tugmasini bosing to'xtatish uchun.")
        app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

    except Exception as e:
        print(f"❌ Xatolik: {e}")


if __name__ == "__main__":  # Tuzatilgan qator
    main()