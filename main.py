import logging.config
import discord
import os
import logging.config
from dotenv import load_dotenv
from os import path
from discord.ext import commands
from flask import Flask
from threading import Thread

app = Flask('')


def bot():
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f'cogs.{filename[:-3]}')

    bot.run(os.getenv('TOKEN'))


@app.route('/')
def home():
    return "Super Pizza Trainer is alive and well! Molto Bene!"


def run():
    app.run(host='0.0.0.0', port=os.getenv('WEBSITES_PORT'))


def web_app():
    t = Thread(target=run)
    t.start()


def main():
    load_dotenv()
    config_path = path.join(path.dirname(path.abspath(__file__)), 'config.ini')
    logging.config.fileConfig(config_path, disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    web_app()
    bot()


if __name__ == '__main__':
    main()
