import re
import random
import datetime
from discord.ext import commands
from private import user_db


class Mail(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mail(self, ctx, usn):
        if ctx.channel.id == 842431863829692416:
            usn.strip()
            pattern = '1(j|J)(b|B)\d\d[a-zA-Z][a-zA-Z]\d\d\d$'
            result = re.match(pattern, usn)

            user = ctx.author
            if result:
                usr_mail = usn + '.sjbit.edu.in'
                mail_res = 'mail verified'
                code = random.randint(100000, 999999)
                j_date = datetime.date.today()
                j_time = datetime.datetime.now().time()
                user_db.newuser(idn=1, uname=str(user), mail=mail_res,
                                passw=str(code), vmail="yes", vpass="no",
                                status=mail_res, join_date=str(j_date),
                                join_time=str(j_time), count=1)

            else:
                mail_res = 'invalid USN: ' + usn
                usr_mail = 'null'
                code = 'null'
            print(f'{mail_res}- {usr_mail}- {user} - {code} ')
        else:
            await ctx.send('The specified command does not work in this channel!')


def setup(bot):
    bot.add_cog(Mail(bot))
