import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
from PIL import ImageGrab
import datetime
import sys

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
chat_id = int(os.getenv("CHAT_ID"))

BOT_TOKEN = bot_token
CHAT_ID = chat_id

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)

logger = logging.getLogger(__name__)

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    USER_ID = update.effective_user.id
    logger.info(f"Received /ping command from user: {USER_ID}")
    if CHAT_ID == USER_ID:
        await update.message.reply_text("Pong!")
        await update.message.reply_text("Welcome to ControlNET v1")
        logger.info(f"Sent 'Pong!' to user ID: {USER_ID}")
    else:
        logger.warning(f"Unauthorized /ping attempt from user ID: {USER_ID}. Ignored.")
        
async def screenshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    USER_ID = update.effective_user.id
    if CHAT_ID == USER_ID:
        try:
            logger.info("Taking Screenshot!")
            img = ImageGrab.grab()
            temp_screenshot_path = f"{sys.platform}_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_screenshot.png"
            img.save(temp_screenshot_path)
            await context.bot.send_photo(chat_id=CHAT_ID, photo=open(temp_screenshot_path, 'rb'), caption='Desktop Screenshot')
            logger.info(f"Sent successfully to {USER_ID}")
        except Exception as e:
            logger.error(f"Cant take screenshot: {e}")
    else:
        logger.warning(f"Different User!")

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()     
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("screenshot", screenshot_command))
    
    logger.info("Bot started. Press Ctrl+C to stop.")
    application.run_polling()
    
if __name__ == '__main__':
    main()