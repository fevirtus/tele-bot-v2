from contextvars import Context
import tracemalloc
from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.commands.debt import DebtCommand
from bot.commands.start import StartCommand
from bot.commands.tft import TFTCommand
from bot.commands.tft_ranked import TFTRankedCommand
from bot.commands.riot import RiotCommand
from bot.commands.home import HomeCommand
from bot.config import Config
from bot.models.inline_button import TFT_RANKED


async def home(update: Update, context: Context):
    if update.message.chat_id == int(Config.HOME_GROUP_ID):
        command = HomeCommand(update, context)
        await command.execute()

async def start(update: Update, context: Context):
    command = StartCommand(update, context)
    await command.execute()

async def debt(update: Update, context: Context):
    command = DebtCommand(update, context)
    await command.execute()

async def tft_ranked(update: Update, context: Context):
    command = TFTRankedCommand(update, context)
    await command.execute()

async def tft(update: Update, context: Context):
    command = TFTCommand(update, context)
    await command.execute()

async def riot(update: Update, context: Context):
    command = RiotCommand(update, context)
    await command.execute()

async def callback_button(update: Update, context: Context):
    query = update.callback_query
    await query.answer()

    if query.data == TFT_RANKED.data:
        await query.edit_message_text(text=f"Selected option: {TFT_RANKED.data}")
        command = TFTRankedCommand(update, context)
        await command.execute()
    elif query.data == 'cmd2':
        await query.edit_message_text(text="Selected option: cmd2")

async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        BotCommand("start", "M ấn thử xem?!!"),
        BotCommand("debt", "Sổ nợ của m đấy"),
        BotCommand("tft", "Teamfight Tactics"),
    ])

def main():
    tracemalloc.start()

    application = Application.builder().token(Config.TELEGRAM_TOKEN).post_init(post_init).build()

    application.add_handler(CommandHandler("home", home))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("debt", debt))
    application.add_handler(CommandHandler("tft", tft))
    application.add_handler(CommandHandler("riot", riot))
    application.add_handler(CallbackQueryHandler(callback_button))

    application.run_polling()

if __name__ == "__main__":
    main()