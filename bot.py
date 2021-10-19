
import os
import sys
import logging
import traceback
from discord.ext import commands
from private import keys

bot = commands.Bot(command_prefix='+')
logg = bot.get_channel(846778354157355109)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author} Please use the correct argument!')
    if isinstance(error, commands.CommandError):
        await ctx.send(f'{ctx.author} Please use the correct command!')


@bot.command()
async def load(ctx, extension):
    try:
        bot.load_extension(f'cogs.{extension}')

        await logg.send('Loaded' + str(extension))
    except Exception as e:
        logging.error(traceback.format_exc())
        await logg.send(f'Error {sys.exc_info()[0]} occurred when loading {extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(keys.TOKEN)
