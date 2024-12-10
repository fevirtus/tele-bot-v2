from riotwatcher import ApiError, RiotWatcher, TftWatcher
from bot.commands.base import BaseCommand
from bot.config import Config
from bot.models.inline_button import TFT_RANKED
from bot.models.tft_user import TFTUser


class RiotCommand(BaseCommand):
    async def execute(self):
        args = self.context.args
        if len(args) != 2:
            await self.bot.send_message(
                    chat_id=self.update.message.chat_id,
                    text="Đ biết đọc à. /riot <tên ingame> <tag>",
                    message_thread_id=self.update.message.message_thread_id
                )
            return
        
        riot_watcher = RiotWatcher(api_key=Config.RIOT_API_KEY)
        game_name = args[0]
        tag_line = args[1]
        try:
            account = riot_watcher.account.by_riot_id(region='asia',game_name=game_name,tag_line=tag_line)
        except ApiError as err:
            if err.response.status_code == 429:
                msg = 'Thử lại sau {} seconds nhé. API thằng riot làm ngu vc'.format(err.response.headers['Retry-After'])
                await self.bot.send_message(
                    chat_id=self.update.message.chat_id,
                    text=msg,
                    message_thread_id=self.update.message.message_thread_id
                )
                return
            elif err.response.status_code == 404:
                msg = 'Không tìm được. Check lại tên ingame và tag đi'
                await self.bot.send_message(
                    chat_id=self.update.message.chat_id,
                    text=msg,
                    message_thread_id=self.update.message.message_thread_id
                )
                return
            else:
                await self.bot.send_message(
                        chat_id=self.update.message.chat_id,
                        text=f"lỗi đ gì ấy:\n{err}",
                        message_thread_id=self.update.message.message_thread_id
                    )
                return
            
        # from puuid get summoner id
        try:
            tft_watcher = TftWatcher(api_key=Config.RIOT_API_KEY)
            tft_user = tft_watcher.summoner.by_puuid(region='vn2', puuid=account['puuid'])
        except ApiError as err:
            if err.response.status_code == 429:
                msg = 'Thử lại sau {} seconds nhé. API thằng riot làm ngu vc'.format(err.response.headers['Retry-After'])
                await self.bot.send_message(
                    chat_id=self.update.message.chat_id,
                    text=msg,
                    message_thread_id=self.update.message.message_thread_id
                )
                return
            else:
                await self.bot.send_message(
                        chat_id=self.update.message.chat_id,
                        text=f"lỗi đ gì ấy:\n{err}",
                        message_thread_id=self.update.message.message_thread_id
                    )
                return

        new_user = TFTUser(
            puuid=account['puuid'],
            gameName=account['gameName'],
            tagLine=account['tagLine']
        )
        new_user.add(self.firebase_client, self.update.message.from_user.id)

        await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text="Xong. 50k nhé",
                message_thread_id=self.update.message.message_thread_id
            )
        return