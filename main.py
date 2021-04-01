import discord
import os
import csv
import time
import logging
import random
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime


DEFAULT_NAME = "Pizza Trainee"
AVATAR_CSV_FILE = "temp/csv_files/avatars.csv"
LOG_FILE = 'pizza_dao_discord.log'
NOOB_CHAT_CHAN_ID = 814164220903161917
JOIN_DA_MAFIA_CHAN_ID = 816405524572536832
PIZZA_NUB_ROLE_ID = 814595921320869909
THRESHOLD = 6 # hours
WELCOME_MSGS = [
  "Welcome to the pizza party, {0}!", 
  "Glad you made it to the pizza party, {0}!", 
  "Good to see you, {0}!",
  "Welcome, {0}. We hope you brought pizza!",
  "{0} just slid into the world's biggest pizza party!",
  "{0} just showed up to the party!",
  "A wild {0} appeared",
  "Welcome, {0}! u hungy?"
]

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

last_timestamp = datetime.min # last time a member joined

def get_member_data(member):
  # id,name,nickname,created_at,joined_at,roles,top_role,avatar_url
  data = [member.id, member.name,  member.nick, member.created_at]
  data.append(member.joined_at if member.joined_at is not None else "")
  data.append("|".join(list(map(lambda role: role.name, member.roles))) if member.roles is not None else "")
  data.append(member.top_role if member.top_role is not None else "")
  data.append(member.avatar_url if member.avatar is not None else "")
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

def get_new_member_msg(name):
  now = datetime.now()
  
  msg = WELCOME_MSGS[random.randint(0, len(WELCOME_MSGS)-1)].format(name)
  if add_channel_link(now):
    msg += "\nDon't forget to head over to <#{0}> to pick ur toitles then report here for ur mafia name".format(JOIN_DA_MAFIA_CHAN_ID)
  
  return msg

@bot.event
async def on_ready():
  logger.info("logged in as {0.user}".format(bot))

@bot.event
async def on_member_join(member):
  logger.info("new member: {0} ({1})".format(member.name, member.mention))
  await member.edit(nick=DEFAULT_NAME)
  noob_chat_chan = bot.get_channel(NOOB_CHAT_CHAN_ID)
  await noob_chat_chan.send(get_new_member_msg(member.mention))

@bot.command(aliases=["csv"])
async def download_csv(ctx):
  logger.info("generating csv file '{0}'".format(AVATAR_CSV_FILE))
  csv_data = []
  csv_cols = ["id", "name", "nickname",  "created_at", "joined_at", "roles", "top_role", "avatar_url"]
  csv_data.append(csv_cols)

  members = bot.guilds[0].members
  for mem in members: 
    row = get_member_data(mem)
    csv_data.append(row)

  create_csv_file(csv_data, AVATAR_CSV_FILE)
  await ctx.send(file=discord.File(AVATAR_CSV_FILE))

@bot.command(aliases=["mc"])
async def member_count(ctx):
  logger.info("member count at {0}".format(ctx.guild.member_count))
  await ctx.channel.send("Total Members: {0}".format(ctx.guild.member_count))


bot.run(os.getenv('TOKEN'))
