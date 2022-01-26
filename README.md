# Prisma Python Discord

This repository contains the source code for the Prisma Python discord bot!

## Setup

```py
python3 -m venv .venv
source .venv/bin/activate
pip install -U -r requirements.txt
```

Create an application on https://discord.com/developers/applications and create a `.env` file with the bot token that Discord gives you:

```
# .env
BOT_TOKEN = "<MY TOKEN>"
```

Setup the database

```
prisma db push
```

Run the bot

```
python -m bot
```
