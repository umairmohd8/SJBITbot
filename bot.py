import os
import sys
import logging
import traceback
from discord.ext import commands
from private import keys

BOT_LOG = 846778354157355109

bot = commands.Bot(command_prefix='+')


"""@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(ctx.author.mention + ' Please use the correct argument!')
    else:
        print('something is wrong')
    if isinstance(error, commands.CommandError):
        await ctx.send(ctx.author.mention + ' Please use the correct command!')
        print()"""


@bot.command()
@commands.has_role('Admin')
async def load(ctx, extension):
    logg = bot.get_channel(BOT_LOG)

    try:
        bot.load_extension(f'cogs.{extension}')
        await logg.send('Loaded ' + str(extension))
    except Exception as e:
        logging.error(traceback.format_exc())
        await logg.send(f'Error {sys.exc_info()[0]} occurred when loading {extension}')


@bot.command()
@commands.has_role('Admin')
async def unload(ctx, extension):
    logg = bot.get_channel(846778354157355109)

    try:
        bot.unload_extension(f'cogs.{extension}')
        await logg.send('Unloaded ' + str(extension))
    except Exception as e:
        logging.error(traceback.format_exc())
        await logg.send(f'Error {sys.exc_info()[0]} occurred when unloading {extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(keys.TOKEN)
