import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

# === CONFIG ===
BOT_TOKEN = "8190809278:AAGvbZ44FhlQmp-6V4Yxa2KboiYeRhExGUo"  # Paste your BotFather token here
FEED_URL = "https://feeds.feedburner.com/crunchyroll/rss/anime"  # change if you want
CHAT_ID = None  # this will be set when user sends /start

latest_title = None

def get_latest_entry():
    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        return None
    entry = feed.entries[0]
    return {"title": entry.title, "link": entry.link}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    await update.message.reply_text("✅ RSS Reader Bot activated! You’ll get updates automatically.")
    print(f"Registered chat ID: {CHAT_ID}")

async def check_feed(bot):
    global latest_title, CHAT_ID
    if CHAT_ID is None:
        return
    entry = get_latest_entry()
    if entry and entry["title"] != latest_title:
        latest_title = entry["title"]
        await bot.send_message(chat_id=CHAT_ID, text=f"🆕 *{entry['title']}*\n{entry['link']}", parse_mode="Markdown")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.create_task(check_feed(app.bot)), "interval", minutes=1)
    scheduler.start()

    print("Bot is running on Render...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
