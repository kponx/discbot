import discord
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.members = True

from discord.ext import commands
bot = commands.Bot(command_prefix="!", intents=intents)

class TarkovCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# ping pong test command
@bot.command()
async def ping(ctx):
  await ctx.channel.send("pong")

 def setup(bot):
    bot.add_cog(TarkovCog(bot))