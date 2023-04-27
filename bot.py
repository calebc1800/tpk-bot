# bot.py
# NOTE: Run directly using python.exe bot.py, vscode debugger will not work
import os
import random

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

# initiative tracker
initiative = {}
initiative_active = False
turn = 0

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
@bot.command(name='r', help='Rolls dice: #d# +/- modifier')
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

# roll initiative
@bot.command(name='init.roll', help='Rolls initiative for a character: !init.roll (modifier) (name)')
async def init(ctx, modifier=0, name=''):
    # check if initiative is active
    if initiative_active:
        await ctx.send('Initiative already started')
        return
    # check for keyword
    if name == '':
        await ctx.send('Input name')
        return
    # check for valid input
    if modifier > MAX_MODIFIER or modifier < -MAX_MODIFIER:
        await ctx.send('Invalid modifier')
        return
    # add to initiative
    initiative[name] = random.randint(1, 20) + int(modifier)
    # send message
    if modifier >= 0:
        await ctx.send(f'{name} rolled {initiative[name] - int(modifier)} + {int(modifier)} = {initiative[name]}')
    else:
        await ctx.send(f'{name} rolled {initiative[name] - int(modifier)} - {abs(int(modifier))} = {initiative[name]}')

# start initiative
@bot.command(name='init.start', help='Starts initiative order: !init.start')
async def start_init(ctx):
    # init global variables
    global turn
    global initiative_active
    global initiative
    # check for keyword
    if len(initiative) == 0:
        await ctx.send('No initiative')
        return
    # send message
    initiative_active = True
    # sort initiative
    initiative = dict(sorted(initiative.items(), key=lambda item: item[1], reverse=True))

    await ctx.send(f'Initiative started... {list(initiative.keys())[turn]} is up first\n')
    # copied from display_init
    # send message
    message = 'Initiative order:\n'
    for key, value in sorted(initiative.items(), key=lambda item: item[1], reverse=True):
        message += f'{key}: {value}'
        if initiative[key] == initiative[list(initiative.keys())[turn]]:
            message += '  <---'
        message += '\n'
    await ctx.send(message)

# display initiative
@bot.command(name='init.display', help='Displays initiative order: !init.display')
async def display_init(ctx):
    # check for keyword
    if len(initiative) == 0:
        await ctx.send('No initiative')
        return
    # send message
    message = 'Initiative order:\n'
    for key, value in sorted(initiative.items(), key=lambda item: item[1], reverse=True):
        message += f'{key}: {value}'
        if initiative[key] == initiative[list(initiative.keys())[turn]]:
            message += '  <---'
        message += '\n'
    await ctx.send(message)

# next turn
@bot.command(name='init.next', help='Moves to next turn: !init.next')
async def next_init(ctx):
    # int global variables
    global turn
    # check for keyword
    if len(initiative) == 0:
        await ctx.send('No initiative')
        return
    # increment turn
    turn = (turn + 1) % len(initiative)
    # send next turn
    await ctx.send(f'Next turn: {list(initiative.keys())[turn]}')
    # copied from display_init
    # send message
    message = 'Initiative order:\n'
    for key, value in sorted(initiative.items(), key=lambda item: item[1], reverse=True):
        message += f'{key}: {value}'
        if initiative[key] == initiative[list(initiative.keys())[turn]]:
            message += '  <---'
        message += '\n'
    await ctx.send(message)

# add to initiative
@bot.command(name='init.add', help='Adds to initiative order: !init.add (modifier) (name)')
async def add_init(ctx, init, name=''):
    # check if initiative is active
    if initiative_active:
        await ctx.send('Initiative already started')
        return
    # check for keyword
    if name == '':
        await ctx.send('Input name')
        return
    # check for valid input
    if int(init) > MAX_MODIFIER or int(init) < -MAX_MODIFIER:
        await ctx.send('Invalid modifier')
        return
    # add to initiative
    initiative[name] = int(init)
    # send message
    await ctx.send(f'{name} added with initiative {init}')

# remove from initiative
@bot.command(name='init.remove', help='Removes from initiative order: !init.remove (name)')
async def remove_init(ctx, name=''):
    # check for keyword
    if name == '':
        await ctx.send('Input name')
        return
    # check if name is in initiative
    if name not in initiative:
        await ctx.send('Name not in initiative')
        return
    # remove from initiative
    initiative.pop(name)
    # send message
    await ctx.send(f'{name} removed')

# clear initiative
@bot.command(name='init.clear', help='Clears initiative order: !init.clear')
async def clear_init(ctx):
    global initiative_active
    # check for keyword
    if len(initiative) == 0:
        await ctx.send('No initiative')
        return
    # clear initiative
    initiative.clear()
    initiative_active = False
    # send message
    await ctx.send('Initiative cleared')

# run bot (leave at bottom)
bot.run(TOKEN)
