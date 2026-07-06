from asyncio import Queue, open_connection
from logging import getLogger

from core.models import CursorOnTarget
from core.utils import transform_cot_to_xml
from settings import Settings


class RawSocketTAKAdapter:
    def __init__(
        self,
        out_queue: Queue[CursorOnTarget],
    ) -> None:
        self.out_queue = out_queue
        self._logger = getLogger("raw_socket")

    def get_host_and_port_from_settings(self) -> tuple[str, str]:
        # not ideal, but should suffice for a simple example
        host, port = Settings.COT_URL.rsplit(":", maxsplit=1)
        return host, port

    async def run(self) -> None:
        host, port = self.get_host_and_port_from_settings()

        if Settings.ATAK_CLIENT_CONSUMER:
            await self._run_for_atak_client(host, port)
        else:
            await self._run_for_atak_server(host, port)


    async def _run_for_atak_client(self, host: str, port: str) -> None:
        """
        ATAK client specifically expects to close the connection before receiving and processing
        the received data. For this unfortunatelly we have to open and close connection for each item
        """
        while True:
            _, writer = await open_connection(host, port)

            try:
                item = await self.out_queue.get()
                self._logger.info("Retrieved next object from queue: %s", item)

                event = transform_cot_to_xml(item)
                self._logger.info("Sending formated CoT: %s", event)
                writer.write(event)
                await writer.drain()

            finally:
                writer.close()
                await writer.wait_closed()

    async def _run_for_atak_server(self, host: str, port: str) -> None:
        _, writer = await open_connection(host, port)

        try:
            while True:
                item = await self.out_queue.get()
                self._logger.info("Retrieved next object from queue: %s", item)

                event = transform_cot_to_xml(item)
                self._logger.info("Sending formated CoT: %s", event)
                writer.write(event)
                await writer.drain()

        finally:
            writer.close()
            await writer.wait_closed()
