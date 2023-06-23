from discord.ext import commands
import config
import asyncio
import discord
import Board

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print('Rigged for silent running')

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         # Ignore if the command is not found
#         return
#     elif isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Missing required arguments.')
#     elif isinstance(error, commands.CheckFailure):
#         await ctx.send('You do not have the required permissions to execute this command.')
#     elif isinstance(error, asyncio.TimeoutError):
#         await ctx.send('Timeout occurred while waiting for a reaction.')
#     else:
#         # Print the error to the console
#         print(f'An error occurred: {error}')

bot.load_extension('ConnectFour')

bot.run(config.bot_token)
