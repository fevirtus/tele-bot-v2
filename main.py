from contextvars import Context
from telegram import Update
from telegram.ext import Application, CommandHandler
from bot.commands.debt import DebtCommand
from bot.config import Config
from bot.commands.start import StartCommand
from bot.commands.info import InfoCommand

async def start(update: Update, context: Context):
    command = StartCommand(update, context)
    await command.execute()

async def info(update: Update, context: Context):
    command = InfoCommand(update, context)
    await command.execute()

async def debt(update: Update, context: Context):
    command = DebtCommand(update, context)
    await command.execute()


def main():
    # Create the application and set the token
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()

    # Register the commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("debt", debt))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()