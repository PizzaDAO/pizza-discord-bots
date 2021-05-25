import logging
import shutil
import discord
from discord.ext import commands
from pathlib import Path
from utils import clean_up
from constants import DISCORD_PROJECTS_CHAN_ID

logger = logging.getLogger(__name__)


class Videos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["videos"])
    async def download_all_videos(self, ctx):
        """
        Downloads all videos in the channel, creates a zipfile containing all videos, 
            and returns the zip file which can be downloaded via discord
        """
        video_types = ["mp4", "webm", "mpg", "mp2", "mpeg", "mpe",
                       "mpv", "ogg", "m4p", "m4v", "avi", "wmv", "qt", "flv", "swf"]
        project_dir = str(Path(__file__).parent.parent)
        videos_dir = project_dir + "/data/videos/"

        count = 0
        async for message in ctx.channel.history():
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(vid_type) for vid_type in video_types):
                    count += 1
                    file_name, file_type = attachment.filename.rsplit(".", 1)
                    # in case files have same name, use count to mark uniqueness
                    file_name += ("_" + str(count) + "." + file_type)
                    file_path = videos_dir + file_name
                    await attachment.save(fp=file_path)

        zip_file_path = project_dir + "/data/discord_videos"
        shutil.make_archive(zip_file_path, 'zip', videos_dir)
        zip_file_path += ".zip"
        try:
            await ctx.send(file=discord.File(zip_file_path))
        except discord.errors.HTTPException as err:
            await ctx.channel.send("Oops, someone dropped the pizza on dis one! We ran into the following error: `{0}`".format(err) +
                                   "\nPlease reach out to the folks over at <#{0}> for help.".format(DISCORD_PROJECTS_CHAN_ID))
        else:
            await ctx.channel.send("Oops, someone dropped the pizza on dis one and we have no clue why :scream:" +
                                   "\nPlease reach out to the folks over at <#{0}> for help.".format(DISCORD_PROJECTS_CHAN_ID))

        # remove all videos and zip file
        clean_up(videos_dir, zip_file_path)


def setup(bot):
    bot.add_cog(Videos(bot))
