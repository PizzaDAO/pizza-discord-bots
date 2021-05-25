import logging
import shutil
import discord
from discord.ext import commands
from pathlib import Path


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
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    count += 1
                    file_name, file_type = attachment.filename.split(".")
                    file_name += ("_" + str(count) + "." + file_type)
                    file_path = images_dir + file_name
                    await attachment.save(fp=file_path)

        zip_file_path = project_dir + "/data/discord_images"
        shutil.make_archive(zip_file_path, 'zip', images_dir)
        await ctx.send(file=discord.File(zip_file_path + ".zip"))


def setup(bot):
    bot.add_cog(Images(bot))
