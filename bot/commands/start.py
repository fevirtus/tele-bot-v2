from bot.commands.base import BaseCommand
from bot.models.user import User

class StartCommand(BaseCommand):
    async def execute(self):
        if User.is_exists(self.firebase_client, self.update.message.from_user.id):
            await self.bot.send_message(
                    chat_id=self.update.message.chat_id,
                    text="Gọi con cậc!",
                    message_thread_id=self.update.message.message_thread_id
                )
            return
        
        # add new user to firestore
        new_user = User(
            id=self.update.message.from_user.id,
            first_name=self.update.message.from_user.first_name,
            last_name=self.update.message.from_user.last_name,
            username=self.update.message.from_user.username,
            is_bot=self.update.message.from_user.is_bot,
            language_code=self.update.message.from_user.language_code
        )
        new_user.add(self.firebase_client)

        # send welcome message
        await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text=f"Nhớ mặt m rồi",
                message_thread_id=self.update.message.message_thread_id
            )
        return
