# Definitions used in cs.creation command

import os
import csv
import discord
from discord.ext import commands

# confirm user input
def confirm(msg):
    if msg.content.lower() != 'yes':
        return False
    else:
        return True