from asyncio import Queue
from configparser import ConfigParser

from pytak import CLITool

from application.pytak.adapter import CoTSender
from core.models import CursorOnTarget
from settings import Settings


async def pytak_setup(out_queue: Queue[CursorOnTarget]) -> CLITool:
    config = ConfigParser()
    config["pytak_setup"] = {
        "COT_URL": Settings.COT_URL,
        "PYTAK_NO_HELLO": Settings.PYTAK_NO_HELLO,
    }

    clitool = CLITool(config["pytak_setup"])
    await clitool.setup()

    clitool.add_tasks(set([CoTSender(clitool.tx_queue, config["pytak_setup"], out_queue)]))

    return clitool

