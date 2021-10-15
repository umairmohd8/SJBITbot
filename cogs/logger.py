import discord
from private import keys
from discord.ext import commands


class Logger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is online')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

    @commands.Bot.event
    async def on_profanity(self, message, word):
        ch = commands.Bot.get_channel(846778354157355109)
        await ch.send('hello')


def setup(bot):
    bot.add_cog(Logger(bot))
