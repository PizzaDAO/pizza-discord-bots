import discord
from discord.ext import commands




class Help(commands.MinimalHelpCommand):


    async def send_command_help(self, command):
        em = discord.Embed(title = command.name, description = command.short_doc)
        em.add_field(name="**How To**", value=command.usage if command.usage else command.signature[1:], inline=False)
        channel = self.get_destination()
        await channel.send(embed=em)

    async def send_bot_help(self, mapping):
        em = discord.Embed(title = "Help", description = "Use $help <command> for extended information on a command. (Case Sensitive)")
        for cog, commands in mapping.items():
            command_names = [c.name for c in await self.filter_commands(commands, sort=True)]
            if command_names: 
                cog_name = getattr(cog, "qualified_name", "No Category")
            if cog_name in "HelpCog": continue
            em.add_field(name="Commands", value="\n".join(command_names), inline=False)
        channel = self.get_destination()
        await channel.send(embed = em)




class HelpCog(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = Help()
        bot.help_command.cog = self
    
    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(HelpCog(bot))