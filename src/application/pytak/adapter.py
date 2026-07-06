import asyncio
import multiprocessing as mp
from configparser import SectionProxy

from pytak import QueueWorker

from core.models import CursorOnTarget
from core.utils import transform_cot_to_xml


class CoTSender(QueueWorker):
    def __init__(self, queue: asyncio.Queue |  mp.Queue, config: None | SectionProxy | dict, out_queue: asyncio.Queue[CursorOnTarget]) -> None:
        super().__init__(queue, config)
        self.out_queue = out_queue

    async def handle_data(self, data: CursorOnTarget):
        """Handle pre-CoT data, serialize to CoT Event, then puts on queue."""
        event = transform_cot_to_xml(data) 
        self._logger.info("Sending formated CoT: %s", event)
        await self.put_queue(event)

    async def run(self):
        """Run the loop for processing or generating pre-CoT data."""
        while True:
            item = await self.out_queue.get()
            self._logger.info("Retrieved next object from queue: %s", item)
            await self.handle_data(item)
