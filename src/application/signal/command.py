from asyncio import Queue

from pydantic import ValidationError
from signalbot import Command, Context, Message

from core.cot.choices import Affiliation
from core.models import TargetPos


class InboundCommand(Command):
    def __init__(self, process_queue: Queue[TargetPos]) -> None:
        super().__init__()
        self.process_queue = process_queue

    async def handle(self, context: Context) -> None:
        try:
            parsed_message = self.parse_message(context.message)
        except ValidationError as err:
            # can be extended with proper error parsing to present a bit more human-readable output
            await self.reject(context, f"Some of the parts are incorrect. Details: {err}")
            return
        except ValueError:
            await self.reject(context, "Message doesn't have enough info")
            return
        
        await self.process_queue.put(parsed_message)
        # react response might look as ok, but actual consumer might fail. this is not ideal
        # in order to handle this case we would have to proxie the consumer response up to signal bot
        # to another command using separate queue that will properly reflect the status of the message
        await context.react("👍")

    async def reject(self, context: Context, message: str) -> None:
        await context.send(message)
        await context.react("👎")

    def parse_message(self, message: Message) -> TargetPos:
        lat, long, description = message.text.split(maxsplit=2)

        affiliation, description = self._extract_affiliation_if_exists(description)

        return TargetPos(coords=(lat, long), description=description, timestamp=message.timestamp, affiliation=affiliation)

    def _extract_affiliation_if_exists(self, target_description: str) -> tuple[Affiliation, str]:
        affiliation, *description = target_description.split()
        
        if not description:
            return Affiliation.UNKNOWN, target_description

        try:
            return Affiliation[affiliation.upper()], " ".join(description)
        except KeyError:
            return Affiliation.UNKNOWN, target_description
