import tanjun
import hikari
from prisma import Client as Prisma, get_client as get_prisma, load_env
from prisma.errors import ClientNotRegisteredError

from .config import Config


async def on_startup() -> None:
    prisma = Prisma(auto_register=True)
    await prisma.connect()


async def on_shutdown() -> None:
    try:
        prisma = get_prisma()
        if prisma.is_connected():
            await prisma.disconnect()
    except ClientNotRegisteredError:
        pass


def load() -> hikari.GatewayBot:
    load_env()
    config = Config.load()
    bot = hikari.GatewayBot(config.bot_token)
    (
        tanjun.Client.from_gateway_bot(bot)
        .load_modules('bot.components.meta')
        .add_prefix(config.prefix)
        .set_type_dependency(hikari.GatewayBot, bot)
        .set_type_dependency(Config, config)
        .add_client_callback(tanjun.ClientCallbackNames.STARTING, on_startup)
        # TODO: I don't know if we actually want to do this
        # .add_client_callback(tanjun.ClientCallbackNames.CLOSING, on_shutdown)
    )
    return bot
