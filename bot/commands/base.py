from contextvars import Context
from telegram import Bot, Update


class BaseCommand:
    def __init__(self, update: Update, context: Context):
        self.update = update
        self.context = context
        self.bot: Bot = context.bot

    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")