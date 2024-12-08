from bot.commands.base import BaseCommand

class InfoCommand(BaseCommand):
    async def execute(self):
        await self.update.message.reply_text("Chào mừng bạn đến với bot Telegram!")
