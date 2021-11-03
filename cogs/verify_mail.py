import re
import random
import datetime

import discord.utils
from discord.ext import commands
from access import mail, newDB

BOT_LOG = 846778354157355109
roles = {'verified': 840568002176614400, 'alum': 902217061692997673, 'first': 842427880675999784,
         'second': 842427873259946023,
         'third': 842427880675999784, 'fourth': 842427886324809768, 'cse': 842426829318258728,
         'ise': 842426832154132534,
         'ece': 842427172609720341, 'eee': 902216757018763306, 'mech': 902248929222090872, 'civ': 902248689786052659}


class Mail(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def verify_mail(self, usn):
        usn.strip()
        pattern = r'1(j|J)(b|B)\d\d[a-zA-Z][a-zA-Z]\d\d\d$'
        result = re.match(pattern, usn)  # checks for a legit usn
        if usn[5:7] == "me" or usn[5:7] == "cv":
            result = False
        return result

    def get_code(self):
        passw = random.randint(100000, 999999)
        return passw

    def assign_roles(self, mail):
        usr_roles = {"year": 0, "branch": 0}
        if int(mail[3:5]) < 18:
            usr_roles["year"] = roles['alum']
        elif int(mail[3:5]) == 18:
            usr_roles["year"] = roles['fourth']
        elif int(mail[3:5]) == 19:
            usr_roles["year"] = roles['third']
        elif int(mail[3:5]) == 20:
            usr_roles["year"] = roles['second']
        elif int(mail[3:5]) == 21:
            usr_roles["year"] = roles['first']

        if mail[5:7] == 'cs':
            usr_roles["branch"] = roles['cse']
        elif mail[5:7] == 'is':
            usr_roles["branch"] = roles['ise']
        elif mail[5:7] == 'ec':
            usr_roles["branch"] = roles['ece']
        elif mail[5:7] == 'ee':
            usr_roles["branch"] = roles['eee']
        elif mail[5:7] == 'me':
            usr_roles["branch"] = roles['mech']
        elif mail[5:7] == 'cv':
            usr_roles["branch"] = roles['civ']

        return usr_roles

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
                # print(lastID[0])

                db_add = newDB.newUser(idn=lastID[0] + 1, uname=str(user), mail=usr_mail,
                                       passw=str(code), vmail=1, vpass=0,
                                       status=mail_res, join_date=str(j_date),
                                       join_time=str(j_time))

                # adding user to db
                if db_add == 0:
                    await self.bot.get_channel(BOT_LOG).send(f'{user.mention} added to db.')

                    # mailing code to user
                    code_res, stat = mail.sendMail(usr_mail, code)
                    if stat == -1:
                        await ctx.send(f'{user.mention} Mail verified, failed to send passcode, dm Admin')
                        await self.bot.get_channel(BOT_LOG).send(f'{user.mention} failed to send passcode, {code_res}')
                    else:
                        await ctx.send(f'{user.mention} Mail verified, passcode sent to your mail(check junk folder)')
                        await self.bot.get_channel(BOT_LOG).send(f'{user.mention} {code_res}')

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
        user = ctx.author
        up_mail = usn + '@sjbit.edu.in'
        print(up_mail)
        up_res = newDB.updateMail(str(ctx.author), up_mail)
        # ADD A FUNCTION TO SEND MAIL AFTER UPDATING MAIL
        up_code = newDB.getPass(str(ctx.author))

        code_res, stat = mail.sendMail(up_mail, up_code[0])
        if stat == -1:
            await ctx.send(f'{user.mention} Mail verified, failed to send passcode, dm Admin')
            await self.bot.get_channel(BOT_LOG).send(f'{user.mention} failed to send passcode, {code_res}')
        else:
            await ctx.send(f'{user.mention} Mail verified, passcode sent to your mail(check junk folder)')
            await self.bot.get_channel(BOT_LOG).send(f'{user.mention} {code_res}')
        await self.bot.get_channel(BOT_LOG).send(f'{ctx.author} {up_res}.')

    @commands.command()
    async def code(self, ctx, passwd):
        user = ctx.author
        db_pass = newDB.getPass(str(user))  # if user not in db , null error
        # adding verified role
        if db_pass[0] == passwd:
            role = discord.utils.get(self.bot.get_guild(ctx.guild.id).roles, id=roles['verified'])
            await user.add_roles(role)
            # adding other roles
            usr_mail = newDB.uMail(str(user))
            print(usr_mail[0])
            oth_roles = self.assign_roles(usr_mail[0])

            year_role = discord.utils.get(self.bot.get_guild(ctx.guild.id).roles, id=oth_roles['year'])
            await user.add_roles(year_role)

            branch = discord.utils.get(self.bot.get_guild(ctx.guild.id).roles, id=oth_roles['branch'])
            await user.add_roles(branch)

            # updating code verification status in db
            pass_stat = newDB.vStat(str(user))
            await self.bot.get_channel(BOT_LOG).send(f'{user} {pass_stat}')
        else:
            await ctx.channel.send(f'{user.mention} passcode did not match!')

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
