import discord
import os
import csv
import time
import logging
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime


DEFAULT_NAME = "Pizza Trainee"
AVATAR_CSV_FILE = "temp/csv_files/avatars.csv"
LOG_FILE = 'pizza_dao_discord.log'
NOOB_CHAT_CHAN_ID = 814164220903161917
JOIN_DA_MAFIA_CHAN_ID = 816405524572536832
THRESHOLD = 1

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
desc = "Download a CSV file that contains Avatar URLs" 
bot = commands.Bot(command_prefix='$', description=desc, intents=intents)

last_timestamp = datetime.now() # last time a member joined

def get_member_data(member):
  # name,nickname,roles,top_role,avatar_url
  data = [member.name,  member.nick] 
  data.append("|".join(list(map(lambda role: role.name, member.roles)))) if member.roles is not None else data.append("")
  data.append(member.top_role) if member.top_role is not None else data.append("")
  data.append(member.avatar_url) if member.avatar is not None else data.append("")
  return data

def create_csv_file(data, filename=AVATAR_CSV_FILE):
  with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
  return

def add_channel_link(now):
  """ calculates the time difference (in hours) since a new member joined
  it returns true if that time difference is greater than THRESHOLD """

  global last_timestamp
  hours = (now - last_timestamp).total_seconds() / (60 * 60)
  logger.info("it's been {0} hours since a member joined".format(hours))
  
  last_timestamp = now
  return (hours >= THRESHOLD)

@bot.event
async def on_ready():
  logger.info("We have logged in as {0.user}".format(bot))

@bot.event
async def on_member_join(member):
  now = datetime.now()

  prev_name = member.name
  await member.edit(nick=DEFAULT_NAME)
  msg = "Welcome to the pizza party, {0}!".format(prev_name)

  if add_channel_link(now):
    msg += " Head over to <#{0}> to pick ur toitles then report here for ur mafia name".format(JOIN_DA_MAFIA_CHAN_ID)
  
  noob_chat_chan = bot.get_channel(NOOB_CHAT_CHAN_ID)
  await noob_chat_chan.send(msg)

@bot.command(name="avatars")
async def download_avatars(ctx):
  logger.info("downloading file '{0}'".format(AVATAR_CSV_FILE))
  csv_data = []
  csv_cols = ["name","nickname","roles","top_role","avatar_url"]
  csv_data.append(csv_cols)

  members = bot.guilds[0].members
  for m in members: 
    row = get_member_data(m)
    csv_data.append(row)

  create_csv_file(csv_data, AVATAR_CSV_FILE)
  await ctx.send(file=discord.File(AVATAR_CSV_FILE))

@bot.command(aliases=["mc"])
async def member_count(ctx):
  add_channel_link(datetime.now())
  logger.info("member count requested ({0})".format(ctx.guild.member_count))
  await ctx.channel.send("Total Members: {0}".format(ctx.guild.member_count))

bot.run(os.getenv('TOKEN'))
