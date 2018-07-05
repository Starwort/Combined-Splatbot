from discord import *
from discord.ext import commands
class RuleCog():
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    async def hs(self,ctx):
        rules = """<:hs1:373194237837312000> **__Hide and seek__** <:hs1:373194237837312000>

TEAM SETUP:
team alpha (with even teams) or smaller team = hiders
team bravo (with even teams) or larger team = seekers

HIDING TIME:
1min for uneven teams (or 45sec on Moray Towers)
45sec for even teams (or 30 on MT)

RESTRICTIONS:
No subs/specials
No map (by extension no super jump)
GAME END:
Hiders win if time is up without all of them having died
Seekers win if all hiders die
Hiding time deaths are excluded
Any seeker that dies may continue
Any hider that dies is out and may only return as a spectator"""
        await ctx.send(rules)
