import discord
from discord.ext import commands
import random

class GifCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter = 0
        self.random_gifs = ["https://cdn.discordapp.com/attachments/655487776657244172/839261047466754088/mark_cuban_rare_pizzas.gif", "https://cdn.discordapp.com/attachments/655487776657244172/839261048766070793/garyv-itis.gif", "https://cdn.discordapp.com/attachments/655487776657244172/839261066265100389/elon-rare-pizzas.gif", "https://cdn.discordapp.com/attachments/655487776657244172/839308737754824714/pizza-drake.gif", "https://cdn.discordapp.com/attachments/655487776657244172/839308816641687552/show_me_the_pizza_maguire.gif", "https://tenor.com/view/pizza-rarepizzas-rarepizzascom-gif-20535144"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.channel.id == (812097286476922943):
                if self.counter == 10:

                    random_gif = self.random_gifs

                    print(self.counter)
                    await message.channel.send(random.choice(random_gif))

                    self.counter = 0 # reset the counter
                else:
                    self.counter += 1



def setup(bot):
    bot.add_cog(GifCog(bot))