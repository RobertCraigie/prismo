from os import environ
from dotenv import load_dotenv

import disnake
from disnake.ext import commands

load_dotenv("../.env")


class BotConfig:
    try:
        token = environ["BOT_TOKEN"]
    except KeyError:
        raise RuntimeError("BOT_TOKEN not found on enviroment variables")
    
    log_level = environ.get("LOG_LEVEL", "DEBUG")
    github_repository = "https://github.com/RobertCraigie/prismo"
    support_server_id = 933860922039099444

    # modifying intents is possible to modify what should be
    # cached by the bot
    intents = disnake.Intents.default()
    intents.message_content = True
    # note that this requires intents.message_content
    command_prefix = commands.when_mentioned_or("p.")
