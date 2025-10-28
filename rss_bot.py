import asyncio
import feedparser
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler

# --- CONFIG ---
TOKEN = "8190809278:AAGvbZ44FhlQmp-6V4Yxa2KboiYeRhExGUo"
CHAT_ID = "1958424381"  # replace with your chat ID
RSS_FEED_URL = "https://feeds.feedburner.com/crunchyroll/rss/anime"
CHECK_INTERVAL = 10  # seconds between RSS checks

# Store already sent entries
sent_entries = set()

# --- BOT SETUP ---
async def start(update, context):
    await update.message.reply_text("RSS Bot is running!")

# --- RSS CHECK ---
async def send_new_entries(app):
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries:
        if entry.id not in sent_entries:
            try:
                await app.bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"New episode: {entry.title}\n{entry.link}"
                )
                sent_entries.add(entry.id)
            except Exception as e:
                print(f"Error sending message: {e}")

# --- PERIODIC TASK ---
async def periodic_rss_check(app):
    while True:
        await send_new_entries(app)
        await asyncio.sleep(CHECK_INTERVAL)

# --- MAIN ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    # Start periodic RSS check
    asyncio.create_task(periodic_rss_check(app))
    
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
