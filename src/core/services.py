import logging
from asyncio import Queue
from datetime import datetime

from core.cot.choices import CotType
from core.models import CursorOnTarget, TargetPos
from settings import Settings

LOGGER_NAME = "core_service"

class CoreService:
    def __init__(self, process_queue: Queue[TargetPos], out_queue: Queue[CursorOnTarget]) -> None:
        self._logger = logging.getLogger(LOGGER_NAME)
        self.process_queue = process_queue
        self.out_queue = out_queue

    async def run(self):
        while True:
            item_to_process = await self.process_queue.get()
            self._logger.info("Received item from process queue: %s", item_to_process)

            processed_item = self.process_item(item_to_process)

            # this is also a place where caching/persistancy mechanism could be added
            # to preserve received items if the consumers will be hanging or the whole 
            # system will be out
            #
            # self.storage_service.save(processed_item)

            await self.out_queue.put(processed_item)
            self._logger.info("Proccesed item successfully and put to out queue: %s", processed_item)

    def process_item(self, item: TargetPos) -> CursorOnTarget:
        item_datetime = self._parse_timestamp(item.timestamp) 
        return CursorOnTarget(
            coords=item.coords,
            description=item.description,
            time=item_datetime,
            start=item_datetime,
            stale=item_datetime + Settings.STALE_OFFSET,
            type=self.resolve_target_cot_type(item.description),
            affiliation=item.affiliation,
        )

    # specifically extracted as a separate method to add possibility to extend this logic
    # in future with a more detailed and sophisticated approach to identify the proper
    # CoT target type. for example based on the https://github.com/dB-SPL/cot-types/blob/main/CoTtypes.xml
    def resolve_target_cot_type(self, target_decsription: str) -> CotType:
        try:
            return CotType[target_decsription.upper()]
        except KeyError:
            return CotType.GROUND  # default cot type

    def _parse_timestamp(self, timestamp: int) -> datetime:
        try:
            return datetime.fromtimestamp(timestamp)
        except ValueError:
            # timestamp could be a ms timestamp instead of seconds
            return datetime.fromtimestamp(timestamp // 1000)
