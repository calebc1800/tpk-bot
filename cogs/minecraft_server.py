from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError

class MinecraftServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # global variables
        load_dotenv()
        INSTANCE_ID = os.getenv('INSTANCE_ID')
        ec2 = boto3.resource('ec2')

    
    # Start the aws ec2 server if user has the role "Minecraft Moderator"
    @commands.command(name="mine.start", help="Starts the Minecraft Server")
    @commands.has_role("Minecraft Moderator")
    async def start_server(self, ctx):
        # TODO: Start the aws ec2 instance
        await ctx.send("Starting the server...")
        try:
            ec2.start_instances(InstanceIds=[INSTANCE_ID], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                await ctx.send("Error starting the server")
                raise
        
        # Dry run succeeded, run start_instances again without dryrun
        try:
            response = ec2.start_instances(InstanceIds=[INSTANCE_ID], DryRun=False)
            await ctx.send(response)
        except ClientError as e:
            await ctx.send(e)
    
    # Stop the aws ec2 server if user has the role "Minecraft Moderator"
    @commands.command(name="mine.stop", help="Stops the Minecraft Server")
    @commands.has_role("Minecraft Moderator")
    async def stop_server(self, ctx):
        # TODO: Stop the aws ec2 instance
        await ctx.send("Stopping the server...")
        try:
            ec2.stop_instances(InstanceIds=[INSTANCE_ID], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                await ctx.send("Error stopping the server")
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            response = ec2.stop_instances(InstanceIds=[INSTANCE_ID], DryRun=False)
            await ctx.send(response)
        except ClientError as e:
            await ctx.send(e)
    
async def setup(bot):
    await bot.add_cog(MinecraftServer(bot))
