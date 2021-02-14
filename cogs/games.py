import random
from discord.ext import commands


class Games(commands.Cog):
    __slots__ = ['client']

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Game is connected.")

    @commands.command(aliases=["8ball", 'życie'])
    async def _8ball(self, ctx, *, question):
        responses = ["Tak", "Nie", "Być może"]
        await ctx.send(f"Pytanie: {question}\n"
                       f"Odpowiedź: {random.choice(responses)}")

    @commands.command(aliases=["rozmiar"])
    async def punkty(self, ctx):
        s = ""
        members = await ctx.guild.fetch_members(limit=150).flatten()
        for member in members:
            s += f"{member.name} ma {random.randint(5, 40)} pkt z RP\n"
        await ctx.send(s)


def setup(client):
    client.add_cog(Games(client))
