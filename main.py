import discord
from discord.ext import commands
from server_logger import ServerLogger

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix = ".")
client=discord.Client(intents=intents)
logger = ServerLogger(bot)

@bot.event
async def on_ready():
    print("online")  
    await bot.change_presence(activity=discord.Game(name="FiveM"))
    await bot.load_extension('bot_commands')
    await bot.load_extension('server_logger')
    await bot.load_extension('captcha_generation')
    await bot.tree.sync()


bot.run("MTA2MjMyMDk1NTU4MzYzMTM3MA.G1u-yW.lgOpEvqdvRZj-n6gP8WhE2fJ609Ms-GsINtkN0")