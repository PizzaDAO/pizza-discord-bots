import logging.config
import discord
import os
import logging.config
from dotenv import load_dotenv
from os import path
from discord.ext import commands


def main():
    load_dotenv()

    config_path = path.join(path.dirname(path.abspath(__file__)), 'config.ini')
    logging.config.fileConfig(config_path, disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix='$', intents=intents)

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f'cogs.{filename[:-3]}')

    bot.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
