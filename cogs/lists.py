from discord import *
from discord.ext import commands
import datetime
from random import choice
class Listing():
    def __init__(self,bot):
        self.bot = bot
    @commands.command(pass_context=True)
    async def lists(self,ctx):
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        embed = Embed(description="The weapon list can be found [here](http://starbright.dyndns.org/starwort/weapon_list.txt),\nthe map list [here](http://starbright.dyndns.org/starwort/map_list.txt),\nand the mode list [here](http://starbright.dyndns.org/starwort/mode_list.txt)", colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_author(name="Lists:", icon_url="https://cdn.discordapp.com/avatars/424540163579052043/b67d194871881f83a7e67f3ed35a02ea.png?size=1024")
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Listing(bot))
