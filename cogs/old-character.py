#Notes: the following values are calculated inside the program: proficency bonus, passive perception, ac, initiative
from discord.ext import commands
import discord
import csv, os
import pandas as pd

class CharacterSheets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Character sheet cog ready')

    @commands.command(name='cs', help='debugging')
    async def cs(self, ctx):
        await ctx.send('Character sheet commands')

    @commands.command(name='cs.create', help='(name) Creates a character sheet')
    async def cs_create(self, ctx, name=''):
        # get member name
        user = ctx.author.name
        # check for keyword
        if name == '':
            await ctx.send('Input name')
            return
        # make folder for user in cs-data if it doesn't exist
        try:
            os.mkdir(f'cs-data/{user}')
        except:
            pass
        cs_path = f'./cs-data/{user}/character-sheet.csv'
        # see if character-sheet.csv exists
        try:
            with open(cs_path, 'r') as file:
                file.close()
        except:
            # create character-sheet.csv from ./templates/character-sheet.csv
            with open('./templates/character-sheet.csv', 'r') as file:
                reader = list(csv.reader(file))
                file.close()
            with open(cs_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerows(reader)
                file.close()
        # check if character sheet already exists
        with open(cs_path, 'r') as file:
            reader = list(csv.reader(file))
            file.close()
            for row in reader:
                if row[0] == name:
                    await ctx.send(f'Character sheet {name} already exists')
                    return
        # create character sheet (wait till all values are collected before writing to file)
        writeToFile = []
        writeToFile.append(name)
        await ctx.send(f'Confirm creation of {name}. You will not be able to stop this process until it is complete. Type "yes" to confirm')
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await self.bot.wait_for('message', check=check)
        if msg.content.lower() != 'yes':
            await ctx.send('Character sheet creation cancelled')
            return
        # race
        await ctx.send('Enter character\'s race')
        msg = await self.bot.wait_for('message', check=check)
        writeToFile.append(msg.content)
        # actual writing to file
        with open(cs_path, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(writeToFile)
        await ctx.send(f'Character sheet {name} created')

async def setup(bot):
    await bot.add_cog(CharacterSheets(bot))
