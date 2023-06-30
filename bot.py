# bot.py
# NOTE: Run directly using python.exe bot.py, vscode debugger will not work
import os
import datetime
import random
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# dice options
MAX_DICE = 100
MAX_SIDES = 100
MAX_MODIFIER = 100

# new member message
@bot.event
async def on_member_join(member):   
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Bot Testing Server!'
    )

# hello
@bot.command(name='hello', help='Responds with a random greeting')
async def hello(ctx):
    # check for keyword
    possible_responses = ['hello', 'hi', 'hey', 'yo', 'sup']
    response = random.choice(possible_responses)
    await ctx.send(response)

# roll dice
@bot.command(name='r', help='#d# +/- mod')
async def roll(ctx, arg, operator='+', modifier=0):
    # check for keyword
    try:
        num_dice, num_sides = map(int, arg.split('d'))
    except:
        # invalid input
        await ctx.send('Invalid input')
        return
    # check for valid input
    if num_dice > MAX_DICE or num_dice < 1 or num_sides > MAX_SIDES or num_sides < 2 or modifier > MAX_MODIFIER or modifier < 0:
        await ctx.send('Invalid input')
        return
    # roll dice
    rolls = [random.randint(1, num_sides) for i in range(num_dice)]
    # send message
    if operator == '+':
        await ctx.send(f'Rolls: {rolls}\nSum: {sum(rolls)} + {modifier} = {sum(rolls) + int(modifier)}')
    elif operator == '-':
        await ctx.send(f'Rolls: {rolls}\nSum: {sum(rolls)} - {modifier} = {sum(rolls) - int(modifier)}')
    else:
        await ctx.send(f'Computing error')

# import cogs
async def load_cogs():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await bot.load_extension(f"cogs.{f[:-3]}")
            #print load with timestamp
            now = datetime.datetime.now()
            print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} INFO     Loaded {f}")

# run bot (leave at bottom)
async def main():
    await load_cogs()
    discord.utils.setup_logging()
    await bot.start(TOKEN)

asyncio.run(main())
