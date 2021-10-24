import re
import random
import datetime

import discord.utils
from discord.ext import commands
from private import newDB

BOT_LOG = 846778354157355109


class Mail(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def verify_mail(self, usn):
        usn.strip()
        pattern = r'1(j|J)(b|B)\d\d[a-zA-Z][a-zA-Z]\d\d\d$'
        result = re.match(pattern, usn)  # checks for a legit usn
        return result

    def get_code(self):
        passw = random.randint(100000, 999999)
        return passw
    def assign_roles(self):


    def send_mail(self):
        pass

    @commands.command()
    async def mail(self, ctx, usn):
        if ctx.channel.id == 842431863829692416:
            res = self.verify_mail(usn)
            user = ctx.author
            # runs only if the pattern is matched
            if res:
                usr_mail = (usn + '@sjbit.edu.in').lower()
                mail_res = 'mail verified'
                # passcode generation
                code = self.get_code()

                j_date = datetime.date.today()
                j_time = datetime.datetime.now().time()

                # getting last ID on the table
                lastID = newDB.last_id()
                print(lastID[0])

                db_add = newDB.newUser(idn=lastID[0] + 1, uname=str(user), mail=usr_mail,
                                       passw=str(code), vmail=1, vpass=0,
                                       status=mail_res, join_date=str(j_date),
                                       join_time=str(j_time))
                if db_add == 0:
                    await self.bot.get_channel(BOT_LOG).send(f'{user.mention} added to db.')

                else:
                    await self.bot.get_channel(BOT_LOG).send(f'{user.mention} failed to add user to db, {db_add}')

            else:
                mail_res = ' invalid USN: ' + usn
                usr_mail = 'null'
                code = 'null'
                await ctx.send(ctx.author.mention + mail_res)
            print(f'{mail_res}- {usr_mail}- {user} - {code} ')
        else:
            await ctx.send('The specified command does not work in this channel!')

    # a user can update his mail with this command when he gets the 'up' role from the mods
    # after verification
    @commands.command()
    @commands.has_role('up')
    async def upmail(self, ctx, usn):
        print(type(ctx.author))
        up_mail = usn + '@sjbit.edu.in'
        print(up_mail)
        up_res = newDB.updateMail(str(ctx.author), up_mail)
        self.send_mail()
        await self.bot.get_channel(BOT_LOG).send(f'{ctx.author} {up_res}.')

    @commands.command()
    async def code(self, ctx, passwd):
        db_pass = newDB.getPass(ctx.author)
        if db_pass[0] == passwd:
            role = discord.utils.get(self.bot.get_guild(ctx.guild.id).roles, id = )
            # adding verifid role



    # command to check if the usn has verified code
    @commands.command()
    @commands.has_any_role('Admin', 'Moderator')
    async def cstat(self, ctx, usn):
        mail = (usn + '@sjbit.edu.in').lower()
        res = newDB.vPass(mail)
        if res[0] == 1:
            await ctx.channel.send(f'{usn} has verified their passcode')
        else:
            await ctx.channel.send(f'{usn} has verified not their passcode')


def setup(bot):
    bot.add_cog(Mail(bot))
