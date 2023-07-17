from discord.ext import commands
import discord
from dotenv import load_dotenv
import os

class MinecraftServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # global variables
        load_dotenv()
        SERVER_IP = os.getenv('MINECRAFT_IP')
        SERVER_PORT = os.getenv('MINECRAFT_PORT')

    
    # Start the aws ec2 server if user has the role "Minecraft Moderator"
    @commands.command(name="mine.start", help="Starts the Minecraft Server")
    @commands.has_role("Minecraft Moderator")
    async def start_server(self, ctx):
        error = False
        # TODO: Start the aws ec2 instance
        if(error == False):
            await ctx.send("Starting the server...")
            await ctx.send("Server is now online!")
        else:
            await ctx.send("Error starting the server")
            # print error code
    
    # Stop the aws ec2 server if user has the role "Minecraft Moderator"
    @commands.command(name="mine.stop", help="Stops the Minecraft Server")
    @commands.has_role("Minecraft Moderator")
    async def stop_server(self, ctx):
        error = False
        # TODO: Stop the aws ec2 instance
        if(error == False):
            await ctx.send("Stopping the server...")
            await ctx.send("Server is now offline!")
        else:
            await ctx.send("Error stopping the server")
            # print error code
    
async def setup(bot):
    await bot.add_cog(MinecraftServer(bot))
