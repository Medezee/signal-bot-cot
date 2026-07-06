import asyncio
import logging

from signalbot import (
    enable_console_logging,
)

from application.raw_sockets.adapter import RawSocketTAKAdapter
from application.signal.bot import init_bot
from core.services import CoreService
from logger import setup_logger
from settings import Settings


async def main():
    enable_console_logging(logging.INFO)
    setup_logger("core_service", logging.INFO)
    setup_logger("raw_socket", logging.INFO)

    process_queue = asyncio.Queue(Settings.MAX_QUEUE_SIZE)
    out_queue = asyncio.Queue(Settings.MAX_QUEUE_SIZE)

    # Signal Bot init
    bot = init_bot(process_queue)
    bot.start(run_forever=False)

    # Core service init
    core_service = CoreService(process_queue, out_queue)

    # PyTAK/TAK init
    # pytak_cli = await pytak_setup(out_queue)

    raw_socket_adapter = RawSocketTAKAdapter(out_queue)

    tasks = [
        asyncio.create_task(core_service.run(), name="core_service"),
        # asyncio.create_task(pytak_cli.run(), name="pytak"),
        asyncio.create_task(raw_socket_adapter.run(), name="raw_socket")
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
