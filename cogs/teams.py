from discord.ext import commands
from discord import *
from random import randint
class Team:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="teams", aliases=["generateTeams","pb"])
    async def generateTeams(self, ctx, *, players: str):
        "Picks random even teams (with necessary spectators) given a pipe (|) separated list of players. e.g.\nrandom|teams player a|player b|player c"
        players = players.split("|")
        noP = len(players)
        if noP < 2 or noP > 10:
            await ctx.send(content="Too many or too few players! (The number of players must fall under (2,10) [interval notation])")
            return
        playersPerSide = min(noP // 2, 4)
        specs = noP - 2 * playersPerSide
        teamA = ["Alpha Team"]
        teamB = ["Bravo Team"]
        spec = []
        for i in range(playersPerSide):
            tmp = randint(0, len(players) - 1)
            teamA.append(players[tmp].strip())
            del players[tmp]
        for i in range(playersPerSide):
            tmp = randint(0, len(players) - 1)
            teamB.append(players[tmp].strip())
            del players[tmp]
        spec = players
        out = ""
        for i in range(playersPerSide + 1):
            out += f"{teamA[i]:^10} | {teamB[i]:^10}\n"
        out += "Spectators\n"
        for i in spec:
            out += f"{i:^10}\n"
        cropped = out.strip("\n")
        await ctx.send(content=f"Teams:```{cropped}```")

def setup(bot):
    bot.add_cog(Team(bot))
