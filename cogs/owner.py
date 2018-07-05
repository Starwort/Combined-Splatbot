from discord.ext import commands
from discord import *
from subprocess import run, PIPE
class OwnerCog:

    def __init__(self, bot):
        self.bot = bot
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            embed = Embed(colour=Colour(0xff0000))
            embed.set_author(name="ERROR")
            embed.add_field(name=type(e).__name__,value=e)
            await ctx.send(embed=embed)
        else:
            embed = Embed(colour=Colour(0x00ff00))
            embed.set_author(name="SUCCESS")
            embed.add_field(name="Successfully loaded",value=cog)
            await ctx.send(embed=embed)


    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            embed = Embed(colour=Colour(0xff0000))
            embed.set_author(name="ERROR")
            embed.add_field(name=type(e).__name__,value=e)
            await ctx.send(embed=embed)
        else:
            embed = Embed(colour=Colour(0x00ff00))
            embed.set_author(name="SUCCESS")
            embed.add_field(name="Successfully unloaded",value=cog)
            await ctx.send(embed=embed)

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            embed = Embed(colour=Colour(0xff0000))
            embed.set_author(name="ERROR")
            embed.add_field(name=type(e).__name__,value=e)
            await ctx.send(embed=embed)
        else:
            embed = Embed(colour=Colour(0x00ff00))
            embed.set_author(name="SUCCESS")
            embed.add_field(name="Successfully reloaded",value=cog)
            await ctx.send(embed=embed)

    @commands.command(name="stop",hidden=True)
    @commands.is_owner()
    async def bot_unload(self, ctx):
        await self.bot.logout()
    @commands.command(name="update",hidden=True)
    @commands.is_owner()
    async def bot_update(self, ctx):
        await ctx.send("```"+run(["git", "pull", "https://github.com/Starwort/Combined-Splatbot.git"], stdout=PIPE,encoding="ASCII").stdout+"```")
        if cog:
            ctx.command = self.cog_reload
            await ctx.reinvoke()
def setup(bot):
    bot.add_cog(OwnerCog(bot))
