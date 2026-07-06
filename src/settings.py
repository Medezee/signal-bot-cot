import os
from datetime import timedelta


class Settings:
    # Signal Bot
    SIGNAL_SERVICE: str = os.environ["SIGNAL_SERVICE"]
    BOT_PHONE_NUMBER: str = os.environ["BOT_PHONE_NUMBER"]

    # Core
    MAX_QUEUE_SIZE: int = int(os.environ.get("MAX_QUEUE_SIZE", 1000)) 
    STALE_OFFSET: timedelta = timedelta(minutes=int(os.environ.get("STALE_OFFSET", 60)))

    # PyTAK/TAK 
    COT_URL: str = os.environ["COT_URL"]
    PYTAK_NO_HELLO: str = "True"

    ATAK_CLIENT_CONSUMER: int = int(os.environ.get("ATAK_CLIENT_CONSUMER", 1))

