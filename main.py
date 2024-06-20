import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import random
import asyncio
from itertools import cycle
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
password = os.getenv("PASSWORD")
uri = f"mongodb+srv://ayaansuddin:{password}@cluster.xlalzgp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.user_messages

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

bot_statuses = cycle(["Status One", "Hello", "Status Code 123", "I'm a bot"])

@tasks.loop(seconds = 1)
async def change_bot_status():
    await bot.change_presence(activity = discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
    print("Bot ready!")
    change_bot_status.start()

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command(aliases = ["gm"])
async def goodmorning(ctx):
    await ctx.send(f"Good morning {ctx.author.mention}!")

@bot.command()
async def gaymeter(ctx):
    gayPercentage = random.randrange(0, 100)
    if gayPercentage > 50:
        await ctx.send(f"{ctx.author.mention} is {gayPercentage}% gay.")
    elif gayPercentage == 50:
        await ctx.send(f"I can't tell if {ctx.author.mention} is gay! They are 50% gay.")
    else:
        await ctx.send(f"{ctx.author.mention} is not gay ({gayPercentage}%).")

@bot.command()
async def fight(ctx):
    await ctx.send("Ping who you want to fight!")
    fightOpp = await bot.wait_for("message")
    checkName = ctx.author.id
    fightOpp = fightOpp.content
    fightOppID = fightOpp[2:-1]
    if str(fightOppID) == str(checkName):
        await ctx.send("You can't fight yourself!")
    else:
        await ctx.send(f"Fighting {fightOpp}!")

@bot.command()
async def sendembed(ctx, usersend):
    embeded_msg = discord.Embed(title = "Title of embed", description = "Description of embed", color = discord.Color.dark_blue())
    embeded_msg.set_thumbnail(url = ctx.author.avatar)
    embeded_msg.add_field(name = "Name of field", value = "Value of field", inline = False)
    embeded_msg.set_image(url = ctx.guild.icon)
    embeded_msg.set_footer(text = "Footer text", icon_url = ctx.author.avatar)
    await ctx.send(embed = embeded_msg)
    await ctx.send(usersend)

@bot.command(name = "store")
async def storeSecret(ctx):
    await ctx.send("Please enter what you would like to store as a secret.")
    message = await bot.wait_for("message")
    db.server_message_log.insert_one (
        {
            "message": message.content,
            "author": message.author.id,
        }
    )
    await ctx.send("Message store successfully!")

#@bot.command()
#async def ping(ctx):
    #ping_embed = discord.Embed(title = "Ping", description = "Latency in ms", color = discord.Color.blue())
    #ping_embed.add_field(name = f"{bot.user.name}'s latency (ms): ", value = f"{round(bot.latency * 1000)}ms.", inline = False)
    #ping_embed.set_footer(text = f"Requested by {ctx.author.name}.", icon_url = ctx.author.avatar)
    #await ctx.send(embed = ping_embed)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)       

asyncio.run(main())