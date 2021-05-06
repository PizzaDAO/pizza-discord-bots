import discord
from discord.ext import commands
from constants import DISCORD_PROJECTS_CHAN_ID


class Help(commands.Cog):
    """
    Returns information about all Modules
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *input):
        """
        Returns information about all Modules if no argument is provided
        If an Module name is provided, it will return information about any available commands
        """

        # if no cog name is passed in as an argument, send information regarding all cogs
        if not input:
            embed = discord.Embed(
                title="Help Guide", color=discord.Color.blue(),
                description=f"Use `$help <module>` to view available commands for that module  :eyes:"
            )

            # iterate over each cog (module) and gather docstrings to use in the overall description
            description = ""
            for cog in self.bot.cogs:
                description += f"`{cog}` {self.bot.cogs[cog].__doc__}\n"
            embed.add_field(name='Modules', value=description, inline=False)

            # add info regarding active development of this bot
            embed.add_field(
                name="About This Bot",
                value=f"This Bot is actively developed by da real pizzaiolos of da PizzaDAO.\n\
                        Chat with us hurr <#{DISCORD_PROJECTS_CHAN_ID}>.\n"
            )

            # add info about where to provide feedback
            embed.set_footer(text=f"To submit feature requests or bugs/issues, please visit our repo at \
                https://github.com/PizzaDAO/pizza-discord-bots")

        # if a module name was provided, send information regarding that cog and any available commands
        elif len(input) == 1:
            for cog in self.bot.cogs:
                # found cog provided by user (capitalization doesn't matter)
                if cog.lower() == input[0].lower():
                    docstring = self.bot.cogs[cog].__doc__
                    description = docstring if docstring is not None else ""
                    commands = [c for c in self.bot.get_cog(cog).get_commands()
                                if not c.hidden]

                    description += "\nAvailable Commands:" if commands is not None else ""

                    embed = discord.Embed(
                        title=f"{cog} Module",
                        description=description,
                        color=discord.Color.green()
                    )

                    # add command info if available
                    for command in commands:
                        if not command.hidden:
                            embed.add_field(
                                name=f"`${command.name}`",
                                value=command.help,
                                inline=False
                            )

                    break  # exit for-else loop since we found the cog the user requested
            else:  # if cog name not found
                embed = discord.Embed(
                    title="Wut in da world is that?!",
                    description=f"I've never heard from a module called `{input[0]}` before!: scream:\
                        Please try `$Help` in order to see a list of available Modules",
                    color=discord.Color.orange()
                )

        # too many cogs names given; we only accept one at a time
        elif len(input) > 1:
            embed = discord.Embed(
                title="Too much pizza for you!!!",
                description="Please provide the name of only one Module at a time :sweat_smile:",
                color=discord.Color.red()
            )

        # send reply containing our embed
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
