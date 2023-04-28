from discord.ext import commands
import random

class InitiativeTracker:
	def __init__(self, bot):
		self.bot = bot
		# set globals
		global MAX_MODIFIER, initiative, initiative_active, turn
		MAX_MODIFIER = 100
		initiative = {}
		initiative_active = False
		turn = 0

    # roll initiative
	@commands.command(name='init.roll', help='Rolls initiative for a character: !init.roll (modifier) (name)')
	async def init(self, ctx, modifier=0, name=''):
		
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
	@commands.command(name='init.start', help='Starts initiative order: !init.start')
	async def start_init(self, ctx):
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
	@commands.command(name='init.display', help='Displays initiative order: !init.display')
	async def display_init(self, ctx):
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
	@commands.command(name='init.next', help='Moves to next turn: !init.next')
	async def next_init(self, ctx):
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
	@commands.command(name='init.add', help='Adds to initiative order: !init.add (modifier) (name)')
	async def add_init(self, ctx, init, name=''):
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
	@commands.command(name='init.remove', help='Removes from initiative order: !init.remove (name)')
	async def remove_init(self, ctx, name=''):
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
	@commands.command(name='init.clear', help='Clears initiative order: !init.clear')
	async def clear_init(self, ctx):
		# check for keyword
		if len(initiative) == 0:
			await ctx.send('No initiative')
			return
		# clear initiative
		initiative.clear()
		initiative_active = False
		# send message
		await ctx.send('Initiative cleared')

def setup(bot):
    bot.add_cog(InitiativeTracker(bot))