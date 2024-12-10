from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.commands.base import BaseCommand
from bot.models.inline_button import TFT_RANKED
from bot.models.tft_user import TFTUser


class TFTCommand(BaseCommand):
    async def execute(self):
        # verify riot account
        if not TFTUser.is_exists(self.firebase_client, self.update.message.from_user.id):
            await self.bot.send_message(
                    chat_id=self.update.message.chat_id,
                    text="Đm t chưa có tk của m\nDùng /riot <tên ingame> <tag> đi. VD: /riot fevirtus 1998\nLúc kết bạn trong game nó kiểu fevirtus#1998 ấy.",
                    message_thread_id=self.update.message.message_thread_id
                )
            return

        keyboard = [
            [InlineKeyboardButton(TFT_RANKED.text, callback_data=TFT_RANKED.data)],
            [InlineKeyboardButton("Lệnh 2", callback_data='cmd2')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text="####",
                message_thread_id=self.update.message.message_thread_id,
                reply_markup=reply_markup
            )