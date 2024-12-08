from telegram import User
from bot.commands.base import BaseCommand
from bot.firebase_service import debt_exists, add_debt, get_debt_by_id
from bot.models.debt import Debt
from bot.utils.utils import debt_to_string, debts_to_dict

class DebtCommand(BaseCommand):
    async def execute(self):
        is_exists = debt_exists(self.update.message.from_user.id)
        if not is_exists:
            add_debt(self.update.message.from_user.id, {})

        # phân tích argument
        args = self.context.args
        if len(args) == 0:
            debts = get_debt_by_id(self.update.message.from_user.id)
            if debts:
                msg = f"Điểm hạnh kiểm:\n{debt_to_string(debts)}"
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
            debts = get_debt_by_id(self.update.message.from_user.id)

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
                debt = next((d for d in debts if d.name == name), None)
                if debt:
                    debt.amount += amount
                else:
                    debts.append(Debt(name=name, amount=amount))

            # update debt
            add_debt(self.update.message.from_user.id, debts_to_dict(debts))
            # get debts and reply
            debts = get_debt_by_id(self.update.message.from_user.id)
            msg = f"Điểm hạnh kiểm:\n{debt_to_string(debts)}"
            await self.bot.send_message(
                chat_id=self.update.message.chat_id,
                text=msg,
                message_thread_id=self.update.message.message_thread_id
            )
            return
