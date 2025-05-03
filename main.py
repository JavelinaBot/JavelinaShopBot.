
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)

CHOOSING, = range(1)

questions = [
    ("Який тип товарів вам більше до вподоби?", ["Для пар", "Для неї", "Для нього"]),
    ("Що для вас важливо?", ["Дизайн", "Функціональність", "Ціна"]),
    ("Який стиль вам ближчий?", ["Романтичний", "Пристрасний", "Ігровий"]),
    ("Який рівень досвіду у вас?", ["Початківець", "Середній", "Просунутий"]),
    ("Що вас цікавить найбільше?", ["Вібратори", "БДСМ", "Масажери", "Інше"]),
]

user_answers = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["step"] = 0
    user_answers[update.effective_user.id] = []
    question, options = questions[0]
    reply_markup = ReplyKeyboardMarkup.from_column(options, resize_keyboard=True)
    await update.message.reply_text(f"{question}", reply_markup=reply_markup)
    return CHOOSING

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step", 0)
    user_id = update.effective_user.id
    user_answers[user_id].append(update.message.text)

    step += 1
    context.user_data["step"] = step

    if step < len(questions):
        question, options = questions[step]
        reply_markup = ReplyKeyboardMarkup.from_column(options, resize_keyboard=True)
        await update.message.reply_text(f"{question}", reply_markup=reply_markup)
        return CHOOSING
    else:
        await update.message.reply_text("Дякуємо за відповіді! Ось товари, які можуть вам сподобатись:")
        await update.message.reply_text("1. Вібратор A | 799 грн")
2. Масажер B | 599 грн
3. Набір для пар C | 999 грн
(Це приклад. Реальні товари можна підтягнути з CSV.)")
        return ConversationHandler.END

def main():
    import os
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)]},
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
