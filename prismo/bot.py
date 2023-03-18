import logging
import datetime

from pathlib import Path

from prisma import Client as Prisma
from prisma.errors import ClientNotRegisteredError
from disnake.ext import commands

from config import BotConfig


class PrismoBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            intents=BotConfig.intents,
            command_prefix=BotConfig.command_prefix,
            case_insensitive=True,
            reload=True,
        )

        self._setup_logging()
        self.prismo_extensions = {"cogs", }

    def _setup_logging(self) -> None:
        self.logger = logging.getLogger("disnake")
        self.logger.setLevel(BotConfig.log_level)
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(logging.Formatter(
            "%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
        self.logger.addHandler(self.handler)

    async def on_ready(self) -> None:
        self.logger.info("Logged in as %s", self.user)

    # note that on_connect and on_disconnect are both called multiple times during bot's
    # lifetime; the reason is that disnake implements reconnection logic
    # so we'll connect and disconnect from the database multiple times during the bot's lifetime
    # this shouldn't particularly affect performances since connect / disconnect events shouldn't be
    # that many
    async def on_connect(self) -> None:
        self.prisma_client = Prisma(auto_register=True)
        self.logger.debug("Connecting to the database")
        await self.prisma_client.connect()

    async def on_disconnect(self) -> None:
        try:
            if self.prisma_client.is_connected():
                self.logger.debug("Disconnecting from the database")
                await self.prisma_client.disconnect()
        except ClientNotRegisteredError:
            pass

    async def start(self) -> None:  # type: ignore
        # we'll use this start time later in the ping command :)
        self.start_time = datetime.datetime.utcnow()
        self.logger.info("Starting the bot")
        self.load_ext()

        await super().start(BotConfig.token, reconnect=True)

    def load_ext(self) -> None:
        for extension_path in self.prismo_extensions:
            path = Path(extension_path).absolute()
            self.load_extensions(path.as_posix())
            self.logger.info(
                "%s extension was successfully loaded", extension_path)
