import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

DEFAULT_NAME = "Pizza Trainee"

load_dotenv()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', description="Download Avatar URLs or actual files", intents=intents)

def get_avatar_urls(guild):
  urls = []
  for count, member in enumerate(guild.members, start=1):
    if member.avatar is not None: urls.append(member.avatar_url)
  return urls

async def extract_files_from_urls(urls):
  s = "s" if len(urls) > 1 else ""

  files = []
  for idx, url in enumerate(urls, start=1): 
    filename = "avatar_{0}.jpg".format(idx)
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

async def send_urls(ctx, urls):
  # char_limit is 2000 but im subtracting 200 to give us a buffer for the last url that 
  # pushes it over the "limit"; got lazy here; will refactor later
  char_limit = 2000 - 200 
  num_urls = len(urls)
  urls_str = ""
  count = 0
  for url in urls: 
    if len(urls_str) >= char_limit: 
      await ctx.channel.send("Avatar URLs ({0}/{1}):\n{2}".format(count, num_urls, urls_str))
      urls_str = ""

    urls_str = ", ".join([urls_str, str(url)]) if urls_str != "" else str(url)
    count += 1
  await ctx.channel.send("Avatar URLs ({0}/{1}):\n{2}".format(count, num_urls, urls_str))

@bot.event
async def on_ready():
  print("We have logged in as {0.user}".format(bot))

@bot.event
async def on_member_join(member):
  prev_name = member.name
  await member.edit(nick=DEFAULT_NAME)

  for c in member.guild.channels:
    if "noob-chat" in str(c):
      await c.send("Welcome to the pizza party, {0}! [formally {1}]".format(member.nick, prev_name))

@bot.command(name="avatars")
async def download_avatars(ctx, content_type="urls"):
  avatar_urls = get_avatar_urls(bot.guilds[0])
  if content_type == "urls": 
    await send_urls(ctx, avatar_urls)
    return 
  
  avatar_files = await extract_files_from_urls(avatar_urls)
  await send_files(ctx, avatar_files)

@bot.command()
async def member_count(ctx):
  await ctx.channel.send("Total Members: {0}".format(ctx.guild.member_count))

bot.run(os.getenv('TOKEN'))
