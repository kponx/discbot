import discord
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.members = True

from discord.ext import commands
bot = commands.Bot(command_prefix="!", intents=intents)

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# ping pong test command
@commands.command()
async def ping(self, ctx):
    await ctx.channel.send("pong")

def setup(bot):
    bot.add_cog(test(bot))