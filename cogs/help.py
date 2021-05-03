import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.group
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Use ?help <command> for extended information on a command. (Case Sensitive)", color = ctx.author.color)
    em.add_field(name = 'Help Commands', value = 'mc,csv')

    await ctx.send(embed = em)


@help.command()
async def mc(ctx):

    em = discord.Embed(title = "mc", description = "Shows The Member Count Of The Pizza Dao Discord", color = ctx.author.color)
    em.add_field(name = "**How To**", value = "$mc")
    
    await ctx.send(embed = em)


@help.command()
async def csv(ctx):

    em = discord.Embed(title = "csv", description = " ", color = ctx.author.color)
    em.add_field(name = "**How To**", value = "$csv")
    
    await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Help(bot))
