from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
import requests

# Загружаем токены из .env
load_dotenv()  

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /twist [сцена], и я придумаю сюжетный поворот.")

async def generate_twist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scene = " ".join(context.args)
    if not scene:
        await update.message.reply_text("Пример: /twist Детектив находит таинственный ключ")
        return
    
    # Запрос к DeepSeek (если API-ключ есть)
    if DEEPSEEK_API_KEY:
        prompt = f"Придумай 3 неочевидных поворота для сцены: «{scene}». Каждый — 1 предложение."
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
        )
        if response.status_code == 200:
            twists = response.json()["choices"][0]["message"]["content"]
            await update.message.reply_text(f"🎭 Варианты:\n{twists}")
            return
    
    # Если DeepSeek недоступен — заглушка
    twists = [
        "1. Ключ ведет не к сокровищу, а к тюремной камере героя.",
        "2. Детектив обнаруживает, что ключ — часть эксперимента по контролю над разумом.",
        "3. В дверце, которую открывает ключ, лежит фотография самого детектива в детстве."
    ]
    await update.message.reply_text("🎭 Варианты:\n" + "\n".join(twists))

# Запуск бота
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("twist", generate_twist))
app.run_polling()