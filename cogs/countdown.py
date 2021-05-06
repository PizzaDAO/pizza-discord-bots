import logging
import datetime
import asyncio
from discord.ext import tasks, commands
from constants import ANNOUNCEMENTS_CHAN_ID

logger = logging.getLogger(__name__)


class Countdown(commands.Cog):
    """
    """

    def __init__(self, bot):
        self.bot = bot
        year = datetime.datetime.now().year
        self.bitcoin_pizza_day = datetime.date(year, 5, 22)  # May 22, 2021 etc
        self.target_hour = 15  # 3pm UTC / 11am EDT / 10am CDT / 8am PDT
        self.message = "Hello @everyone!! Today is {date}, which means there are **{days} DAYS until May 22**, Bitcoin Pizza Day! Let's goooo!"
        self.announcement.start()

    def cog_unload(self):
        self.announcement.cancel()

    @tasks.loop(hours=24)
    async def announcement(self):
        today = datetime.date.today()
        days = (self.bitcoin_pizza_day - today).days

        today_str = today.strftime("%B %d, %Y")
        message = self.message.format(date=today_str, days=(days-1))
        logger.info("making announcement with message: '{0}'".format(message))
        announcements_chan = self.bot.get_channel(ANNOUNCEMENTS_CHAN_ID)
        await announcements_chan.send(message)

    @announcement.before_loop
    async def before_announcement(self):
        logger.info("waiting until the bot is ready")
        await self.bot.wait_until_ready()
        logger.info("bot is ready; waiting to start announcement task")
        await self.wait_until_target_time()
        logger.info("kicking off announcement task")

    async def wait_until_target_time(self):
        today = datetime.datetime.utcnow()
        logger.info("today is {0}".format(today))
        target_time = today.replace(hour=self.target_hour, minute=0,
                                    second=0, microsecond=0)
        logger.info("target_time is {0}".format(target_time))

        if today >= target_time:
            target_time += datetime.timedelta(days=1)
            logger.info("passed target hour so schedule task kick off until next day ({0})".
                        format(target_time))

        sleepy_time = (target_time - today).total_seconds()
        logger.info("doin a snooze for {0} seconds".format(sleepy_time))
        await asyncio.sleep(sleepy_time)


def setup(bot):
    bot.add_cog(Countdown(bot))
