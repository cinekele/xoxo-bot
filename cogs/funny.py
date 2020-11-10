import discord
import os
import praw
import time
import random
import pyttsx3
from discord.ext import commands, tasks


class Funny(commands.Cog):
    __slots__ = ['client', 'reddit', 'top_memes', 'top_boobs', 'players', 'engine']

    def __init__(self, client):
        self.client = client
        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')
        user_agent = os.getenv('user_agent')
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent=user_agent)
        self.top_memes = None
        self.top_boobs = None
        self.players = {}
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun is connected.")
        self.papiezowa_godzina.start()

    @commands.command()
    async def hello_there(self, ctx):
        await ctx.send(f"General Kenobi!", tts=True)

    @commands.command()
    async def ziobro(self, ctx):
        """ Funkcja mówiaca słynne słowa Stonogi """
        await self.play(ctx, "Ziobro.mp3")

    @commands.command()
    async def student(self, ctx):
        await self.play(ctx, "student.mp4")

    async def play(self, ctx: discord.ext.commands.Context, source):
        channel = ctx.author.voice.channel
        if channel is None:
            await ctx.send("Musisz być na kanale głosowym")
        else:
            voice_client = await self.connect_voice_client_to_channel(channel)
            sound = discord.FFmpegPCMAudio(source=source,
                                           executable=r"C:\Users\PC-Komputer\Documents\ffmpeg\bin\ffmpeg.exe")
            await voice_client.play(sound)

    async def connect_voice_client_to_channel(self, channel: discord.VoiceChannel):
        if channel.guild.id in self.players:
            voice_client = self.players[channel.guild.id]
        else:
            voice_client = await channel.connect()
            self.players[channel.guild.id] = voice_client
        return voice_client

    @commands.command()
    async def boobs(self, ctx):
        if not self.top_boobs:
            self.top_boobs = list(self.reddit.subreddit("Boobies").hot(limit=40))
        which_boobs = random.randint(0, len(self.top_boobs) - 1)
        await ctx.send(self.top_boobs[which_boobs].url)
        self.top_boobs.pop(which_boobs)

    @commands.command()
    async def tts(self, ctx, *, arg):
        self.engine.save_to_file(arg, 'test.mp4')
        self.engine.runAndWait()
        await self.play(ctx, 'test.mp4')

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.guild.id in self.players:
            voice_client = self.players.pop(ctx.guild.id)
            await voice_client.disconnect()
        else:
            await ctx.send("Musisz być na kanale z botem głosowym")

    @tasks.loop(minutes=1)
    async def memes(self, channel: discord.TextChannel):
        if not self.top_memes:
            self.top_memes = list(self.reddit.subreddit('memes').hot(limit=40))
        await channel.send(self.top_memes[-1].url)
        self.top_memes.pop()

    @tasks.loop(minutes=1)
    async def papiezowa_godzina(self):
        if time.localtime().tm_hour == 21 and time.localtime().tm_min == 37:
            for guild in self.client.guilds:

                proper_channel = guild.system_channel if guild.system_channel is not None else False
                if proper_channel:
                    await guild.system_channel.send(":flag_va: Papieżowa godzina :flag_va:")
                    await guild.system_channel.send(":two: :one: :three: :seven:", tts=True)

                max_members, voice_channel_with_max_members = 0, None
                for voice_channel in guild.voice_channels:
                    number_of_members = len(voice_channel.voice_states)
                    if number_of_members > max_members:
                        max_members = number_of_members
                        voice_channel_with_max_members = voice_channel

                if max_members > 0:
                    voice_client = await self.connect_voice_client_to_channel(voice_channel_with_max_members)
                    sound = discord.FFmpegPCMAudio(source="Barka - Krzysztof Krawczyk.mp3",
                                                   executable=r"C:\Users\PC-Komputer\Documents\ffmpeg\bin\ffmpeg.exe")
                    await voice_client.play(sound)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:
            if member.id == 300370298287685632:
                sound = discord.FFmpegPCMAudio(source='karakan.mp3',
                                               executable=r"C:\Users\PC-Komputer\Documents\ffmpeg\bin\ffmpeg.exe")
            else:
                nazwa = member.nick if member.nick is not None else member.name
                self.engine.save_to_file(f"{nazwa} dołączył do kanału", 'test.mp4')
                self.engine.runAndWait()
                sound = discord.FFmpegPCMAudio(source='test.mp4',
                                           executable=r"C:\Users\PC-Komputer\Documents\ffmpeg\bin\ffmpeg.exe")
            voice_client = await self.connect_voice_client_to_channel(after.channel)
            try:
                await voice_client.play(sound)
            except:
                pass

    @commands.command()
    async def start(self, ctx):
        await ctx.send("Pętla z memami się rozpoczęła")
        if not self.top_memes:
            self.top_memes = list(self.reddit.subreddit('memes').hot(limit=40))
        self.memes.start(ctx.channel)

    @commands.command()
    async def stop(self, ctx):
        await ctx.send("Pętla z memami się skończyła")
        self.memes.stop()

    @commands.command()
    async def mute(self, ctx):
        if ctx.author.voice.channel is not None:
            users = ctx.author.voice.channel.members
            for user in users:
                await user.edit(mute=True)

    @commands.command()
    async def gadaj(self, ctx):
        if ctx.author.voice.channel is not None:
            users = ctx.author.voice.channel.members
            for user in users:
                await user.edit(mute=False)


def setup(client):
    client.add_cog(Funny(client))
