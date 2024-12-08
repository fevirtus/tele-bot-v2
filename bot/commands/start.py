from telegram import User
from bot.commands.base import BaseCommand
from bot.firebase_service import user_exists, add_user

class StartCommand(BaseCommand):
    async def execute(self):
        is_exists = user_exists(self.update.message.from_user.id)
        if is_exists:
            await self.bot.send_message(
                    chat_id=self.update.message.chat_id,
                    text="Đăng ký rồi, start cc!",
                    message_thread_id=self.update.message.message_thread_id
                )
            
            return
        
        new_user = User(
            id=self.update.message.from_user.id,
            first_name=self.update.message.from_user.first_name,
            last_name=self.update.message.from_user.last_name,
            username=self.update.message.from_user.username,
            is_bot=self.update.message.from_user.is_bot,
            language_code=self.update.message.from_user.language_code
        )

        add_user(new_user)
        await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text=f"Đăng ký xong.\nChào {self.update.message.from_user.first_name}, thử cái gì đó đi",
                message_thread_id=self.update.message.message_thread_id
            )
        
        return
