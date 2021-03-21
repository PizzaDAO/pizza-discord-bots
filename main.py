import discord
import os
from dotenv import load_dotenv

DEFAULT_NAME = "Pizza Trainee"

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))  

@client.event
async def on_member_join(member):
  prev_name = member.name
  await member.edit(nick=DEFAULT_NAME)

  for c in member.guild.channels:
    if "noob-chat" in str(c):
      await c.send("Welcome to the pizza party, {0}! [formally {1}]".format(member.nick, prev_name))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("!pingpizzapaltraineebot" ):
    # just to test that it's up and running
    await message.channel.send("molto bene!")

client.run(os.getenv('TOKEN'))
