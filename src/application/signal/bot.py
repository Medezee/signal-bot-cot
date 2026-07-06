from asyncio import Queue

from signalbot import Config, SignalBot

from application.signal.command import InboundCommand
from core.models import TargetPos
from settings import Settings


def init_bot(process_queue: Queue[TargetPos]) -> SignalBot:
    bot = SignalBot(
                Config(
                    signal_service=Settings.SIGNAL_SERVICE,
                    phone_number=Settings.BOT_PHONE_NUMBER,
                    )
                )
    bot.register(InboundCommand(process_queue)) 

    return bot
