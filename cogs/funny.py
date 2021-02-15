import asyncio
from multiprocessing import Queue
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
                                  user_agent=user_agent,
                                  check_for_async=False)
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

    async def play(self, channel: discord.VoiceChannel, source):
        voice_client, queue = await self.connect_voice_client_to_channel(channel)
        if voice_client.is_playing():
            queue.put(source)
        else:
            sound = discord.FFmpegPCMAudio(source=source,
                                           executable=r"ffmpeg.exe")
            voice_client.play(sound, after=lambda x: None if queue.empty() else self.play_next(channel, queue.get()))

    def play_next(self, channel, source):
        asyncio.run_coroutine_threadsafe(self.play(channel, source), self.client.loop)

    async def connect_voice_client_to_channel(self, channel: discord.VoiceChannel):
        if channel.guild.id in self.players:
            voice_client, queue = self.players[channel.guild.id]
        else:
            voice_client = await channel.connect(timeout=2.0, reconnect=True)
            queue = Queue()
            self.players[channel.guild.id] = (voice_client, queue)
        return voice_client, queue

    @commands.command()
    async def boobs(self, ctx):
        if not self.top_boobs:
            self.top_boobs = list(self.reddit.subreddit("Boobies").hot(limit=40))
        which_boobs = random.randint(0, len(self.top_boobs) - 1)
        await ctx.send(self.top_boobs[which_boobs].url)
        self.top_boobs.pop(which_boobs)

    @commands.command()
    async def tts(self, ctx, *, arg):
        self.engine.save_to_file(arg, r'music/test.mp4')
        self.engine.runAndWait()
        await self.play(ctx, r'music/test.mp4')

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
                    await self.play(voice_channel_with_max_members, r"music/Barka.mp3")


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and member != self.client.user:
            if member.id == 300370298287685632:
                await self.play(after.channel, r"music/karakan.mp3")
            else:
                nazwa = member.nick if member.nick is not None else member.name
                self.engine.save_to_file(f"Na kanał wbija jak na bombsajt A: {nazwa}", r'music/test.mp4')
                self.engine.runAndWait()
                await self.play(after.channel, r"music/test.mp4")
        if member == self.client.user:
            if after.channel is None:
                self.players.pop(before.channel.guild.id)

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
    async def ziobro(self, ctx):
        """ Funkcja mówiaca słynne słowa Stonogi """
        await self.play(ctx.channel, r"music/ziobro.mp3")

    @commands.command()
    async def student(self, ctx):
        await self.play(ctx.channel, r"music/student.mp4")

    @commands.command()
    async def jeszcze(self, ctx):
        await self.play(ctx.author.voice.channel, 'music/jeszcze.mp3')

    @commands.command()
    async def sesja(self, ctx):
        await self.play(ctx.author.voice.channel, 'music/sesja.mp3')

    @commands.command()
    async def zaliczenie(self, ctx):
        await self.play(ctx.author.voice.channel, 'music/zaliczenie.mp3')

    @commands.command()
    async def kutas(self, ctx):
        await self.play(ctx.author.voice.channel, 'music/kutas.mp3')

    @commands.command()
    async def niewiem(self, ctx):
        await self.play(ctx.author.voice.channel, 'music/niewiem.mp3')

    @commands.command()
    async def brama(self, ctx):
        await self.play(ctx.author.voice.channel, 'music/wypierdalaj.mp3')

    @commands.command()
    async def grzecznie(self, ctx):
        await self.play(ctx.author.voice.channel, 'music/grzecznie.mp3')

    @commands.command()
    async def ulica(self, ctx):
        await self.play(ctx.author.voice.channel, 'music/z_ulicy.mp3')

    @commands.command(aliases=["gadaj"])
    async def unmute(self, ctx):
        if ctx.author.voice.channel is not None:
            users = ctx.author.voice.channel.members
            for user in users:
                await user.edit(mute=False)


def setup(client):
    client.add_cog(Funny(client))
