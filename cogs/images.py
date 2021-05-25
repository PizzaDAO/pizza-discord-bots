import logging
import shutil
import discord
from discord.ext import commands
from pathlib import Path
from utils import clean_up
from constants import DISCORD_PROJECTS_CHAN_ID

logger = logging.getLogger(__name__)


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["images"])
    async def download_all_images(self, ctx):
        """
        Downloads all images in the channel, creates a zipfile containing all images, 
            and returns the zipfile which can be downloaded via discord
        """
        image_types = ["png", "jpeg", "jpg"]
        project_dir = str(Path(__file__).parent.parent)
        images_dir = project_dir + "/data/images/"

        count = 0
        async for message in ctx.channel.history():
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(img_type) for img_type in image_types):
                    count += 1
                    file_name, file_type = attachment.filename.rsplit(".", 1)
                    # in case files have same name, use count to mark uniqueness
                    file_name += ("_" + str(count) + "." + file_type)
                    file_path = images_dir + file_name
                    await attachment.save(fp=file_path)

        zip_file_path = project_dir + "/data/discord_images"
        shutil.make_archive(zip_file_path, 'zip', images_dir)
        zip_file_path += ".zip"
        try:
            await ctx.send(file=discord.File(zip_file_path))
        except discord.errors.HTTPException as err:
            await ctx.channel.send("Oops, someone dropped the pizza on dis one! We ran into the following error: `{0}`".format(err) +
                                   "\nPlease reach out to the folks over at <#{0}> for help.".format(DISCORD_PROJECTS_CHAN_ID))
        else:
            await ctx.channel.send("Oops, someone dropped the pizza on dis one and we have no clue why :scream:" +
                                   "\nPlease reach out to the folks over at <#{0}> for help.".format(DISCORD_PROJECTS_CHAN_ID))
        # remove all images and zip file
        clean_up(images_dir, zip_file_path)


def setup(bot):
    bot.add_cog(Images(bot))
