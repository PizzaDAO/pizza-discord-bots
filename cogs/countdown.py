import logging
import datetime
import asyncio
import random
from discord.ext import tasks, commands
from constants import ANNOUNCEMENTS_CHAN_ID, HYPE_MSGS

logger = logging.getLogger(__name__)


class Countdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        year = datetime.datetime.utcnow().year
        self.bitcoin_pizza_day = datetime.date(year, 5, 22)
        self.tau_day = datetime.date(year, 6, 28)
        self.target_hour = 15  # 3pm UTC / 11am EDT / 10am CDT / 8am PDT
        self.messages = {
            "0522": "Hello @everyone! Today is {date}, which means there are **{days} DAYS until May 22nd**, Bitcoin Pizza Day! {hype}",
            "0628": "Hello @everyone! Today is {date}, which means there are **{days} DAYS until June 28th**, Tau Day! {hype}",
            "default": "Oops, looks like my circuits got mixed up. Today is {date}; days is {days}; hype message is {hype}. Haaalp debug me!",
        }
        self.announcement.start()

    def cog_unload(self):
        self.announcement.cancel()

    @tasks.loop(hours=24)
    async def announcement(self):
        # bitcoin pizza day, tau day, or next year
        today = datetime.date.today()
        target_day = datetime.date(1959, 10, 31)
        if today <= self.bitcoin_pizza_day:
            target_day = self.bitcoin_pizza_day
        elif today <= self.tau_day:
            target_day = self.tau_day
        else:
            target_day = datetime.date(today.year + 1, 5, 22)  # next year

        days = (target_day - today).days
        if days > 42:
            # start countdown for next years bitcoin pizza days 42 days before
            # this is to limit noise in channel; 30 days is too boring. 42 is the answer.
            return

        message_key = target_day.strftime("%m%d")
        today_str = today.strftime("%B %d, %Y")
        hype_msg = HYPE_MSGS[random.randint(0, len(HYPE_MSGS)-1)]
        message = self.messages.get(message_key, self.messages["default"]).format(
            date=today_str, days=days, hype=hype_msg)

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
