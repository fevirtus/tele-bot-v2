from bot.commands.base import BaseCommand
from bot.models.debt import Debt
from bot.models.debt_list import DebtList

class DebtCommand(BaseCommand):
    async def execute(self):
        list_debt = DebtList(self.firebase_client, self.update.message.from_user.id)

        # phân tích argument
        args = self.context.args
        if len(args) == 0:
            debts = list_debt.debts
            if len(debts) == 0:
                msg = "Chẳng có thằng nào nợ m cả :'<"
                await self.bot.send_message(
                    chat_id=self.update.message.chat_id,
                    text=msg,
                    message_thread_id=self.update.message.message_thread_id
                )
                return
            msg = f"Điểm hạnh kiểm:\n{list_debt.to_string()}"
            await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text=msg,
                message_thread_id=self.update.message.message_thread_id
            )
            return
        elif len(args) % 2 == 1:
            await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text="Sai cú pháp. /debt <tên> <số tiền>",
                message_thread_id=self.update.message.message_thread_id
            )
            return
        else:
            # even index is name, odd index is amount
            for i in range(0, len(args)-1, 2):
                name = args[i]
                try:
                    amount = int(args[i + 1])
                except ValueError:
                    await self.bot.send_message(
                        chat_id=self.update.message.chat_id,
                        text="Sai cú pháp. /debt <tên> <số tiền>",
                        message_thread_id=self.update.message.message_thread_id
                    )
                    return
                list_debt.update(Debt(name, amount))

            msg = f"Điểm hạnh kiểm:\n{list_debt.to_string()}"
            await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text=msg,
                message_thread_id=self.update.message.message_thread_id
            )
            return
