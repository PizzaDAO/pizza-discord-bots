import discord
import os
import csv
import time
import logging
from dotenv import load_dotenv
from discord.ext import commands

DEFAULT_NAME = "Pizza Trainee"
AVATAR_CSV_FILE = "data/csv_files/avatars.csv"
AVATAR_IMGS_FILE_DIR = "data/images/"
LOG_FILE = 'pizza_dao_discord.log'

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
desc = "Download Avatar URLs via a CSV file or actual img files" # csv is recommended to not spam discord chan
bot = commands.Bot(command_prefix='$', description=desc, intents=intents)


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
  
async def extract_files_from_urls(urls):
  files = []
  for idx, url in enumerate(urls, start=1): 
    filename = AVATAR_IMGS_FILE_DIR + "avatar_{0}.jpg".format(idx)
    await url.save(filename)
    files.append(discord.File(fp=filename))
  return files

async def send_files(ctx, files):
  send_files_limit = 10
  num_files = len(files)
  for i in range(0, num_files, send_files_limit):
    start = i + 1
    end = i + send_files_limit 
    if end >= num_files: end = num_files
    await ctx.channel.send("Avatar Files {0} through {1} of {2}".format(start, end, num_files), files=files[i:end])

@bot.event
async def on_ready():
  logger.info("We have logged in as {0.user}".format(bot))

@bot.event
async def on_member_join(member):
  prev_name = member.name
  await member.edit(nick=DEFAULT_NAME)

  # sometimes member.nick is None so maybe sleep 
  # to ensure changes are committed? todo: investigate this more
  time.sleep(1) 
  for c in member.guild.channels:
    if "noob-chat" in str(c):
      await c.send("Welcome to the pizza party, {0} ({1})!]".format(member.nick, prev_name))

@bot.command(name="avatars")
async def download_avatars(ctx, content_type="csv"):
  logger.info("downloading avatars as {0}".format(content_type))
  csv_data = []
  csv_cols = ["name","nickname","roles","top_role","avatar_url"]
  csv_data.append(csv_cols)

  members = bot.guilds[0].members
  for m in members: 
    row = get_member_data(m)
    csv_data.append(row)

  if content_type in ["csv", "urls"]:
    create_csv_file(csv_data, AVATAR_CSV_FILE)
    await ctx.send(file=discord.File(AVATAR_CSV_FILE))
    return 

  data = csv_data[1:] # remove header rows
  urls = list(filter(lambda x: x != "", map(lambda row: row[-1], data))) # extract non empty avatar_url column values
  avatar_files = await extract_files_from_urls(urls)
  await send_files(ctx, avatar_files)

@bot.command()
async def member_count(ctx):
  logger.info("member count requested ({0})".format(ctx.guild.member_count))
  await ctx.channel.send("Total Members: {0}".format(ctx.guild.member_count))


bot.run(os.getenv('TOKEN'))
