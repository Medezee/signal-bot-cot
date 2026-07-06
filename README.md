# Signal Bot with TAK integration

A small project that handles the integration between Signal messanger bot and different consumers for [Cursor-on-Target](https://www.mitre.org/sites/default/files/pdf/09_4937.pdf) data. The program itself is done with hexagonal approach to ease the process of connecting new consumers/producers services. 

In this example Signal Bot producer was developed + TAK server/client consumers based on [PyTAK](https://github.com/snstac/pytak/) and raw socket connection on pure python. 

Example includes a suggested local TAK server in `taky-server` based on [TAKy](https://github.com/tkuester/taky) server implementation.

# Installation & Running Locally

## Requirements 

- Signal Account that could be used as a bot
- [Docker](https://docs.docker.com/engine/install/) & [docker-compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/) (3.12+) + [uv](https://docs.astral.sh/uv/) (suggested)
- [ATAK](https://www.civtak.org/download-atak/) or any other client

## Installation

1. First Signal CLI RestAPI should be started. Please follow the [guide](https://signalbot-org.github.io/signalbot/latest/getting_started/#setup-signal-cli-rest-api) to start it. Make sure you have an available Signal account that could be used as a bot.
2. Configure TAK client/server:
    - **Option 1. TAK Client**
        1. In case you want to use client directly make sure the MESH network is enabled. For example in ATAK you should go to `Settings -> Network Preferences -> Network Connection Preferences`
        2. Remember the `My Primary IP Address`.
        3. Scroll down `Input/Output Management` section and make sure `Enable Mesh Network Mode` is enabled.
        4. Go to `Manage Inputs` tab and check what port is set in `Default TCP` item. By default it should be `4242`. Remember it.

    - **Option 2. TAK Server**

        1. If you already have a TAK server, perfect. Remember the password + port where your server receives CoT data and set it in the environment variables later.
        2. If not, use one small server bundled within this project. Go to `taky-server` directory and run following commands:
        ```sh
        cd taky-server  # if you're not there yet
        docker compose up --build -d  # to lauch the taky server as a docker container
        ```
        3. Now go to your TAK Client and add this server there. Use `<host-ip>` as a server address and chose `TCP` connection option on `8087` port, no SSL and no user authentication.

3. Configure [`env.sh`](env.sh) environment variables. 
    - set `COT_URL` to TAK Client IP address with a proper TCP port in case of **Option 1** from previous step and set them in the next uncommented lines:
    ```sh 
    # Uncomment this part if you want to send data to ATAK client directly
    export COT_URL=<My Primary Ip Address>:<Default TCP Port>
    export ATAK_CLIENT_CONSUMER=1
    ```
    - Otherwise uncomment next lines:
    ```sh 
    # Uncomment if you want to use TAKy server
    export COT_URL=localhost:8087  # if you are using your own TAK server, specify it's address and port
    export ATAK_CLIENT_CONSUMER=0 
    ```
4. Set signal account bot number in `PHONE_NUMBER` variable. Example: `+380123456789`
5. *(Optional)*. If you need to change the marker stale time or the max queue size, uncomment `MAX_QUEUE_SIZE` and `SLATE_OFFSET` variables and set the needed values.
6. Everything should be ready now. To start the project run next commands:
```sh
uv sync
un run src/main.py`
```

# Libraries & Tools
- [Docker](https://docs.docker.com/engine/install/) & [docker-compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/) (3.12+) + [uv](https://docs.astral.sh/uv/) (suggested)
- [PyTAK](https://github.com/snstac/pytak/)
- [TAKy](https://github.com/tkuester/taky)
