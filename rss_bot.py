from telegram.ext import Application, CommandHandler
import asyncio
import feedparser
import time

BOT_TOKEN = "8190809278:AAGvbZ44FhlQmp-6V4Yxa2KboiYeRhExGUo"
RSS_URL = "https://feeds.feedburner.com/crunchyroll/rss/anime"
CHAT_ID = "1958424381"  # your Telegram user ID or group ID

def start(update, context):
    update.message.reply_text("✅ RSS Reader Bot activated!")

def fetch_rss(context):
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        return
    latest_entry = feed.entries[0]
    title = latest_entry.title
    link = latest_entry.link
    context.bot.send_message(chat_id=CHAT_ID, text=f"📰 *{title}*\n{link}", parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Run the job every 5 minutes
    app.job_queue.run_repeating(fetch_rss, interval=300, first=10)

    print("Bot is running on Render...")
    app.run_polling()  # synchronous, no async loop issues

if __name__ == "__main__":
    main()
