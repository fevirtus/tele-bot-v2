from bot.commands.base import BaseCommand
from bot.models.home import Home
from bot.config import Config
from bot.models.user import User
from google.cloud import firestore

from bot.utils.utils import convert_to_vnd


class HomeCommand(BaseCommand):
    async def execute(self):
        members_id = Config.HOME_MEMBERS.split(',')
        if str(self.update.message.from_user.id) not in members_id:
            await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text=" không phải là thành viên trong cái nhà này",
                message_thread_id=self.update.message.message_thread_id
            )

        home_members: list[Home] = []
        for member_id in members_id:
            home_members.append(Home.get(self.firebase_client, member_id))

        # phân tích argument
        args = self.context.args
        if len(args) == 0:
            text = all_members_to_str(self.firebase_client)
            await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text=text,
                message_thread_id=self.update.message.message_thread_id
            )
            return
        if len(args) == 1:
            if not args[0].isdigit() or int(args[0]) <= 0:
                await self.bot.send_message(
                    chat_id=self.update.message.chat_id,
                    text="Sai cú pháp. /home <số nguyên dương>",
                    message_thread_id=self.update.message.message_thread_id
                )
                return
            # plus debt for other members
            arg = int(args[0])
            for member in home_members:
                if member.user_id != self.update.message.from_user.id:
                    member.plus(self.firebase_client, arg / len(home_members))

            text = all_members_to_str(self.firebase_client)
            await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text=text,
                message_thread_id=self.update.message.message_thread_id
            )
            return
        if len(args) == 2:
            if args[0] != 'debt' or int(args[1]) == 0:
                await self.bot.send_message(
                    chat_id=self.update.message.chat_id,
                    text="Sai cú pháp. /home debt <số tiền>",
                    message_thread_id=self.update.message.message_thread_id
                )
                return
            # plus debt for member who send the command
            arg = int(args[1])
            for member in home_members:
                if member.user_id == self.update.message.from_user.id:
                    member.plus(self.firebase_client, arg)

            text = all_members_to_str(self.firebase_client)
            await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text=text,
                message_thread_id=self.update.message.message_thread_id
            )
            return

        # send welcome message
        await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text=f"Sai cú pháp",
                message_thread_id=self.update.message.message_thread_id
            )
        return


def all_members_to_str(client: firestore.Client) -> str:
    members_id = Config.HOME_MEMBERS.split(',')
    home_members: list[Home] = []
    for member_id in members_id:
        home_members.append(Home.get(client, member_id))

    text = "Sổ nợ nhà:\n"
    for member in home_members:
        u = User.get(client, member.user_id)
        if u:
            debt = convert_to_vnd(member.debt)
            text += f"{u.first_name} {u.last_name}: {debt}\n"
    return text