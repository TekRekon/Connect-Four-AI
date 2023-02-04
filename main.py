from discord.ext import commands
import config

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print('Rigged for silent running')

bot.load_extension('connectfour')
print("ConnectFour initiated")

bot.run(config.bot_token)
