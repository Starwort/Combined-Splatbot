from discord import *
from discord.ext import commands
class RuleCog():
    def __init__(self,bot):
        self.bot = bot
    @commands.command(aliases=['hideandseek','hideseek','h&s','hide&seek'])
    async def hs(self,ctx):
        '''Lists the rules of Hide and Seek'''
        rules = """<:hs1:373194237837312000> **__Hide and seek__** <:hs1:373194237837312000>

GAME SETUP:
Turf War
Map of the players' choice (or randomised)

TEAM SETUP:
Team Alpha (with even teams) or smaller team = hiders
Team Bravo (with even teams) or larger team = seekers

HIDING TIME:
1min for uneven teams (or 45sec on Moray Towers)
45sec for even teams (or 30 on MT)

RESTRICTIONS:
No subs/specials
No map (by extension no super jump)
Any *hider* that dies is out and may only return as a spectator
Any *seeker* that dies may CONTINUE to seek

GAME END:
Hiders win if time is up without all of them having died
Seekers win if all hiders die
Hiding time deaths are excluded"""
        await ctx.send(rules)
    @commands.command(aliases=['lasertag','lazertag'])
    async def lt(self, ctx):
        '''Lists the rules of Laser Tag'''
        rules = '''<:lt:464854837549334540> **__Laser Tag__** <:lt:464854837549334540>

GAME SETUP:
Recommended Clam Blitz, or Turf War can be used
Map of the players' choice (or randomised)

TEAM SETUP:
May use either even or uneven teams - uneven teams changes scoring

RESTRICTIONS:
All players must use a non-scoped charger - if the host wishes this may be restricted further to a specific charger
Subs and specials are disallowed - resulting in DQ if used
Map and super jump are ALLOWED

GAME END AND SCORING:
Game ends at 5:00 (or 3:00 if Turf War was selected) at which point nobody may kill anyone and one team will break the basket to end the game.
The results are read from SplatNet2 - each player's statistics will read `<kills> [(assists)] <deaths> <specials>`
The scores for the players are then calculated as `kills - assists` - this is their true number of kills
For even teams the team's score is simply the total of each player's score
For uneven teams the team's score is the total of each player's score divided by the number of players on the team
The team or, if agreed upon before the game, player with the most points wins'''
        await ctx.send(rules)
    @commands.command(aliases=['tacticalturfwar','tw'])
    async def ttw(self, ctx):
        '''Lists the rules of Tactical Turf War'''
        rules = '''<:ttw:477223858148081664> **__Tactical Turf War__** <:ttw:477223858148081664>

GAME SETUP:
Turf War, any map (players agree or randomised)

TEAM SETUP:
Any number of players from 2 to 8, balanced teams.

HOW TO PLAY:
The game is played just like a normal turf war, with splatting, inking turf, and no restrictions on player movement and spawn times.
HOWEVER
Each player must ink 590p of turf BUT ALSO must NOT ink more than 600p.

WHO WINS:
If any player failed to meet 590p or exceeded 600p, their team loses. If both teams had a player who did not meet the conditions, then *everyone* loses.
If neither team had players outside of the range, then the winner is the winner of the normal Turf War.'''
        await ctx.send(rules)
def setup(bot):
    bot.add_cog(RuleCog(bot))
