import os
from itertools import cycle

import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix='.', intents=discord.Intents().all())

activities = cycle([discord.Activity(type=discord.ActivityType.watching, name='porno'),
                    discord.Activity(type=discord.ActivityType.listening, name="Janusza Korwina Mikke"),
                    discord.Activity(type=discord.ActivityType.watching, name="dzbanienie Freja"),
                    discord.Activity(type=discord.ActivityType.playing, name="walenie gruchy"),
                    discord.CustomActivity('Daje hedziki w CS:GO')])


@client.event
async def on_ready():
    change_status.start()
    print(f"{client.user} is ready.\n")


@tasks.loop(minutes=1)
async def change_status():
    await client.change_presence(activity=next(activities))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Ta komenda nie istnieje")


@client.command()
async def load(ctx, extension):
    if ctx.author.name == "cinek" and ctx.author.discriminator == "3508":
        client.load_extension(f"cogs.{extension}")
    else:
        await ctx.send("You have no power here.")


@client.command()
async def unload(ctx, extension):
    if ctx.author.name == "cinek" and ctx.author.discriminator == "3508":
        client.unload_extension(f"cogs.{extension}")
    else:
        await ctx.send("You have no power here.")


@client.command()
async def reload(ctx, extension):
    if ctx.author.name == "cinek" and ctx.author.discriminator == "3508":
        client.reload_extension(f"cogs.{extension}")
    else:
        await ctx.send("You have no power here.")


@client.command(aliases=["kobieta", "wyczysc"])
async def clear(ctx, amount: int):
    if amount < 0:
        await ctx.send("Nie da się skasować ujemne liczby wiadomości.")
    else:
        await ctx.channel.purge(limit=amount+1)


@client.command()
async def shutdown(ctx):
    if ctx.author.name == "cinek" and ctx.author.discriminator == "3508":
        await client.close()
    else:
        await ctx.send("You have no power here.")


@tasks.loop(hours=20)
async def forms():
    for guild in client.guilds:
        await guild.system_channel.send("Proszę serdecznie o wypełnienie ankiety")
        await guild.system_channel.send("https://forms.gle/zRh67WrbBPchmyoP7")


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Proszę sprecyzować dodatnią liczbę wiadomości do usunięcia.")

for filename in os.listdir(r"cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
