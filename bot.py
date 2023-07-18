# bot.py
# NOTE: Run directly using python.exe bot.py, vscode debugger will not work
import os
import datetime
import random
import asyncio
import discord
import logging
import boto3
from discord.ext import commands
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CREATOR_ID = os.getenv('CREATOR_ID')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Server variables
global MINECRAFT_INSTANCE_ID, BOT_INSTANCE_ID, ec2
MINECRAFT_INSTANCE_ID = os.getenv('MINECRAFT_INSTANCE_ID')
BOT_INSTANCE_ID = os.getenv('BOT_INSTANCE_ID')
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
ec2 = boto3.client('ec2', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# dice options
MAX_DICE = 100
MAX_SIDES = 100
MAX_MODIFIER = 100

# new member message
@bot.event
async def on_member_join(member):   
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {GUILD}!'
    )

# hello
@bot.command(name='hello', help='Responds with a random greeting')
async def hello(ctx):
    # check for keyword
    possible_responses = ['hello', 'hi', 'hey', 'yo', 'sup']
    response = random.choice(possible_responses)
    await ctx.send(response)

# random quote
@bot.command(name='quote', help='Responds with a random quote')
async def quote(ctx):
    # reads a line from quotes.txt
    with open('quotes.txt', 'r') as f:
        lines = f.readlines()
        response = random.choice(lines)
    f.close()
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

# STSSD
@bot.command(name='stssd', help='A special command only to be used by the creator')
async def stssd(ctx):
    # check for keyword
    if ctx.author.id == 221426191796535299:
        await ctx.send('Time to shut the shit show down')
        # shutdown both the bot server and minecraft server
        try:
            response = ec2.stop_instances(InstanceIds=[MINECRAFT_INSTANCE_ID], DryRun=False)
            await ctx.send("Mine closed")
        except ClientError as e:
                await ctx.send("Can't stop the mine!")
        try:
            await ctx.send("Fairwell my friends")
            response = ec2.stop_instances(InstanceIds=[BOT_INSTANCE_ID], DryRun=False)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                await ctx.send("Well shit, that didn't work.")
                raise
    else:
        await ctx.send('You are not the creator')

# import cogs
async def load_cogs():
    # load only minecraft_server cog till others are finished
    await bot.load_extension("cogs.minecraft_server")
    #print load with timestamp
    now = datetime.datetime.now()
    print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} INFO     Loaded minecraft_server.py")
""" # load all cogs    
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await bot.load_extension(f"cogs.{f[:-3]}")
            #print load with timestamp
            now = datetime.datetime.now()
            print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} INFO     Loaded {f}")"""

# run bot (leave at bottom)
async def main():
    await load_cogs()
    discord.utils.setup_logging()
    await bot.start(TOKEN)

asyncio.run(main())
