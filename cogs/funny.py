import asyncio
from multiprocessing import Queue
import discord
import time
import pyttsx3
from discord.ext import commands, tasks


class Funny(commands.Cog):
    __slots__ = ['client', 'reddit', 'top_memes', 'top_boobs', 'players', 'engine']

    def __init__(self, client):
        self.client = client
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
        voice_client, queue, loop = await self.connect_voice_client_to_channel(channel)
        if voice_client.is_playing():
            queue.put(source)
        else:
            sound = discord.FFmpegPCMAudio(source=source,
                                           executable=r"ffmpeg.exe")

            def after(error):
                if loop:
                    queue.put(source)
                return None if queue.empty() else self.play_next(channel, queue.get())

            voice_client.play(sound, after=lambda x: after(x))

    def play_next(self, channel, source):
        asyncio.run_coroutine_threadsafe(self.play(channel, source), self.client.loop)

    async def connect_voice_client_to_channel(self, channel: discord.VoiceChannel):
        if channel.guild.id in self.players:
            voice_client, queue, loop = self.players[channel.guild.id]
        else:
            voice_client = await channel.connect(timeout=2.0, reconnect=True)
            queue = Queue()
            loop = False
            self.players[channel.guild.id] = (voice_client, queue, loop)
        return voice_client, queue, loop

    @commands.command()
    async def loop(self, ctx):
        if ctx.guild.id in self.players:
            voice_client, queue, loop = self.players.get(ctx.guild.id)
        loop = True
        self.players.update({ctx.guild.id: (voice_client, queue, loop)})

    @commands.command()
    async def unloop(self, ctx):
        if ctx.guild.id in self.players:
            voice_client, queue, loop = self.players.get(ctx.guild.id)
        loop = False
        self.players.update({ctx.guild.id: (voice_client, queue, loop)})

    @commands.command()
    async def tts(self, ctx, *, arg):
        self.engine.save_to_file(arg, r'music/test.mp4')
        self.engine.runAndWait()
        await self.play(ctx, r'music/test.mp4')

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.guild.id in self.players:
            voice_client = self.players.pop(ctx.guild.id)[0]
            await voice_client.disconnect()
        else:
            await ctx.send("Musisz być na kanale z botem głosowym")

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
                server_id = before.channel.guild.id
                if server_id in self.players:
                    self.players.pop(server_id)
            if after.afk:
                voice_client = self.players.get(before.channel.guild.id)[0]
                await voice_client.disconnect()


    @commands.command(aliases=["next"])
    async def skip(self, ctx):
        """Pomiń audio"""
        voice_client = self.players[ctx.guild.id][0]
        if voice_client.is_playing():
            voice_client.stop()

    @commands.command()
    async def ziobro(self, ctx):
        """Funkcja mówiaca słynne słowa Stonogi"""
        await self.play(ctx.author.voice.channel, r"music/ziobro.mp3")

    @commands.command()
    async def student(self, ctx):
        """Smutna historia pewnego studenta"""
        await self.play(ctx.author.voice.channel, r"music/student.mp4")

    @commands.command()
    async def jeszcze(self, ctx):
        """Jeszcze jak"""
        await self.play(ctx.author.voice.channel, 'music/jeszcze.mp3')

    @commands.command()
    async def sesja(self, ctx):
        """Opowieść o trudnych czasach"""
        await self.play(ctx.author.voice.channel, 'music/sesja.mp3')

    @commands.command()
    async def zaliczenie(self, ctx):
        """Piosenka o trudnym studenckim życiu"""
        await self.play(ctx.author.voice.channel, 'music/zaliczenie.mp3')

    @commands.command()
    async def kutas(self, ctx):
        """Brakuje ci dużego ..."""
        await self.play(ctx.author.voice.channel, 'music/kutas.mp3')

    @commands.command()
    async def niewiem(self, ctx):
        """No nie wiem byczku"""
        await self.play(ctx.author.voice.channel, 'music/niewiem.mp3')

    @commands.command()
    async def brama(self, ctx):
        """Kolejny cytat wybitnego polaka"""
        await self.play(ctx.author.voice.channel, 'music/wypierdalaj.mp3')

    @commands.command()
    async def grzecznie(self, ctx):
        """Jeszcze się zastanawiasz??"""
        await self.play(ctx.author.voice.channel, 'music/grzecznie.mp3')

    @commands.command()
    async def ulica(self, ctx):
        """Uliczny chłopak"""
        await self.play(ctx.author.voice.channel, 'music/z_ulicy.mp3')

    @commands.command(aliases=["gadaj"])
    async def unmute(self, ctx):
        """Odcisz kanał"""
        if ctx.author.voice.channel is not None:
            users = ctx.author.voice.channel.members
            for user in users:
                await user.edit(mute=False)

    @commands.command()
    async def mute(self, ctx):
        """Wycisz kanał"""
        if ctx.author.voice.channel is not None:
            users = ctx.author.voice.channel.members
            for user in users:
                await user.edit(mute=True)


def setup(client):
    client.add_cog(Funny(client))
