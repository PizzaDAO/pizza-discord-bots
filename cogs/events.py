import discord
import logging
from discord.ext import commands
from datetime import datetime
from constants import DEFAULT_NAME, JOIN_DA_MAFIA_CHAN_ID, NOOB_CHAT_CHAN_ID
from utils import generate_welcome_message, time_exceeded

logger = logging.getLogger(__name__)


class Events(commands.Cog):
    """
    Handles the following events: 
    - Bot Start Up: Sets bot activity.
    - New Member: Greets new members.
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member_join_timestamp = datetime.min

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("logged in as {0.user}".format(self.bot))
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='People Eat Pizza'))
        # Change the line above for the status

    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = datetime.now()
        logger.info("new member: {0} ({1})".format(
            member.name, member.mention))
        await member.edit(nick=DEFAULT_NAME)

        msg = generate_welcome_message(member.mention)
        if time_exceeded(self._last_member_join_timestamp, now):
            msg += "\nDon't forget to head over to <#{0}> to pick ur toitles then report here for ur mafia name".format(
                JOIN_DA_MAFIA_CHAN_ID)
            self._last_member_join_timestamp = now

        noob_chat_chan = self.bot.get_channel(NOOB_CHAT_CHAN_ID)
        await noob_chat_chan.send(msg)


def setup(bot):
    bot.add_cog(Events(bot))
