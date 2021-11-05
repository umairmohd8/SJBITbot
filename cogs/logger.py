from discord.ext import commands
import datetime


class Logger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.chann = 846778354157355109

    @commands.Cog.listener()
    async def on_ready(self):
        ch = self.bot.get_channel(self.chann)
        await ch.send('Bot is online: ' + str(datetime.datetime.now()))
        print('bot is online: ' + str(datetime.datetime.now()))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong! {0}s'.format(round(self.bot.latency,1)))


def setup(bot):
    bot.add_cog(Logger(bot))
