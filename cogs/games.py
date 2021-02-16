import os
import discord
from discord.ext import commands, tasks
import praw
import random


class Games(commands.Cog):
    __slots__ = ['client']

    def __init__(self, client):
        self.client = client
        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')
        user_agent = os.getenv('user_agent')
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent=user_agent,
                                  check_for_async=False)
        self.top_memes = None
        self.top_boobs = None

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

    @commands.command()
    async def start(self, ctx):
        """Wystartuj pętle z memami"""
        await ctx.send("Pętla z memami się rozpoczęła")
        if not self.top_memes:
            self.top_memes = list(self.reddit.subreddit('memes').hot(limit=40))
        self.memes.start(ctx.channel)

    @commands.command()
    async def stop(self, ctx):
        """Skońcź pętle z memami"""
        await ctx.send("Pętla z memami się skończyła")
        self.memes.stop()

    @tasks.loop(minutes=1)
    async def memes(self, channel: discord.TextChannel):
        if not self.top_memes:
            self.top_memes = list(self.reddit.subreddit('memes').hot(limit=40))
        await channel.send(self.top_memes[-1].url)
        self.top_memes.pop()

    @commands.command()
    async def boobs(self, ctx):
        if not self.top_boobs:
            self.top_boobs = list(self.reddit.subreddit("Boobies").hot(limit=40))
        which_boobs = random.randint(0, len(self.top_boobs) - 1)
        await ctx.send(self.top_boobs[which_boobs].url)
        self.top_boobs.pop(which_boobs)



def setup(client):
    client.add_cog(Games(client))
