#Thanks to https://github.com/AHiddenDonut/Economy-Bot-Youtube for databse tutorial
import asyncio
import sys
import aiohttp
import requests
from discord.ext import commands
import random
import discord
import sqlite3
from discord_components import *


def get_random_color():
    return random.choice([0x4287f5, 0xf54242, 0xf5f242])


async def open_acc(user):
    db = sqlite3.connect('bank.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if result:
        return
    if not result:
        sql = "INSERT INTO main(member_id, wallet, bank,gold,diamonds,silver,staff,machine) VALUES(?,?,?,?,?,?,?,?)"
        val = (user.id, 500, 0, 0, 0, 0, 0, 0)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


async def remove_bal(user: discord.Member, amount: int):
    db = sqlite3.connect('bank.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET wallet = ? WHERE member_id = ?"
    val = (result[1] - amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


async def remove_bankbal(user: discord.Member, amount: int):
    db = sqlite3.connect('bank.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET bank = ? WHERE member_id = ?"
    val = (result[2] - amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


async def add_bal(user: discord.Member, amount: int):
    db = sqlite3.connect('bank.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET wallet = ? WHERE member_id = ?"
    val = (result[1] + amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


async def r_diamonds(user: discord.Member, amount: int):
    db = sqlite3.connect('bank.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET diamonds = ? WHERE member_id = ?"
    val = (result[4] - amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


async def r_gold(user: discord.Member, amount: int):
    db = sqlite3.connect('bank.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET gold = ? WHERE member_id = ?"
    val = (result[3] - amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


async def r_silver(user: discord.Member, amount: int):
    db = sqlite3.connect('bank.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET silver = ? WHERE member_id = ?"
    val = (result[5] - amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


async def add_bankbal(user: discord.Member, amount: int):
    db = sqlite3.connect('bank.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET bank = ? WHERE member_id = ?"
    val = (result[2] + amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


async def add_bag(user: discord.Member, amount: int, amount1: int,
                  amount2: int):
    db = sqlite3.connect('bank.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    #sql = f"UPDATE main SET gold = ?,diamonds = ?,silver = ? WHERE member_id = ?"
    #val = (result[3] + amount,result[4] + amount1,result[5] + amount2, user.id)
    sql = f"UPDATE main SET gold = ? WHERE member_id = ?"
    val = (result[3] + amount, user.id)
    cursor.execute(sql, val)
    sql = f"UPDATE main SET diamonds = ? WHERE member_id = ?"
    val = (result[4] + amount1, user.id)
    cursor.execute(sql, val)
    sql = f"UPDATE main SET silver = ? WHERE member_id = ?"
    val = (result[5] + amount2, user.id)
    cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()


class Bank(commands.Cog):
    """Returns random results"""
    def __init__(self, client):
        self.client = client
        DiscordComponents(client)

    #----------------------------Bank--------------------------#
    @commands.command(aliases=['balance', 'bank'])
    async def bal(self, ctx: commands.Context, member: discord.Member = None):
        if member == None:
            member = ctx.author
        await open_acc(member)
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE member_id = {member.id}")
        result = cursor.fetchone()

        embed = discord.Embed(color=get_random_color(),
                              timestamp=ctx.message.created_at)
        embed.set_author(name=f"{member.name}'s Balance",
                         icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Wallet",
                        value=f"`{result[1]} INR`",
                        inline=False)
        embed.add_field(name="Bank", value=f"`{result[2]} INR`", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.send(embed=embed)

    #wallet=1 bank=2

    @commands.command(name="dep", aliases=['deposit'])
    async def dep(self, ctx: commands.context, amount=None):
        await open_acc(user=ctx.author)
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()
        if int(amount) <= 1:
            return await ctx.send("Amount shouldn't be negative lol!")
        if result[1] == 0:
            return await ctx.send("Low balance!")
        if amount == "max":
            sql = "UPDATE main SET bank = ? WHERE member_id = ?"
            val = (0, ctx.author.id)
            await add_bankbal(ctx.author, result[2])
            await remove_bal(ctx.author, result[1])
            await ctx.send(f"You successfully withdrawn **{result[2]}** ")

        else:
            amt = int(amount)
            await open_acc(user=ctx.author)
            db = sqlite3.connect('bank.db')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT * FROM main WHERE member_id = {ctx.author.id}")
            result = cursor.fetchone()
            if result[1] < amt:
                return await ctx.send("Low balance")
            cursor.close()
            await remove_bal(ctx.author, amt)
            await add_bankbal(ctx.author, amt)

            await ctx.send(f"Successfully deposited **{amount}**!")

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    # wallet=1 bank=2

    @commands.command(aliases=['wd'])
    async def withdraw(self, ctx: commands.context, amount: str):
        await open_acc(user=ctx.author)
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()
        if int(amount) <= 1:
            return await ctx.send("Amount shouldn't be negative lol!")
        if result[2] == 0:
            return await ctx.send("Low balance")
        if amount == "max":
            sql = "UPDATE main SET bank = ? WHERE member_id = ?"
            val = (0, ctx.author.id)
            await add_bal(ctx.author, result[2])
            await remove_bankbal(ctx.author, result[2])
            await ctx.send(f"You successfully withdrawn **{result[2]}** ")

        else:
            amt = int(amount)
            if result[2] < amt:
                return await ctx.send("Low balance")
            await add_bal(ctx.author, amt)
            await remove_bankbal(ctx.author, amt)
            await ctx.send(f"Successfully withdrawn **{amount}**!")

    @commands.command()
    async def send(self,
                   ctx: commands.context,
                   member: discord.Member = None,
                   amount=None):
        if member == None:
            return await ctx.send(
                "Please mention user whom you want to transfer money!")
        if int(amount) <= 1:
            return await ctx.send("Amount shouldn't be negative lol!")
        else:
            await open_acc(member)
            amt = int(amount)
            await open_acc(user=ctx.author)
            db = sqlite3.connect('bank.db')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT * FROM main WHERE member_id = {ctx.author.id}")
            result = cursor.fetchone()
            if result[2] < amt:
                return await ctx.send("Low balance")
            cursor.close()
            await remove_bankbal(ctx.author, amt)
            await add_bankbal(member, amt)

            await ctx.send("Successfully sent!")

    #--------------------------spin---------------------#

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def tada(self, ctx: commands.context, amount=None):
        await open_acc(ctx.author)
        amt = int(amount)
        if amount == None:
            await ctx.send("use format p!tada <amount> " +
                           ctx.message.author.name)
            return
        if int(amount) <= 1:
            return await ctx.send("Amount shouldn't be negative lol!")
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()
        if result[1] < amt:
            return await ctx.send("Low wallet balance")
        final = []

        for i in range(3):
            a = random.choice([
                ":test_tube:", ":tada:", ":moneybag:", ":tokyo_tower:",
                ":airplane:", ":kite:", ":helicopter:"
            ])
            final.append(a)
        s1 = str(final[0])
        s2 = str(final[1])
        s3 = str(final[2])
        if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
            await add_bal(ctx.author, int(amount))
            emb = discord.Embed(description="**Won!**    " +
                                ctx.message.author.name + "\n\n" + "[ " + s1 +
                                " , " + s2 + " , " + s3 + " ]\n")
            # await ctx.send("**WON! **" + ctx.message.author.mention)
            await ctx.send(embed=emb)
        else:
            await remove_bal(ctx.author, int(amount))
            emb = discord.Embed(description="**Lost!**    " +
                                ctx.message.author.name + "\n\n" + "[ " + s1 +
                                " , " + s2 + " , " + s3 + " ]\n")
            # await ctx.send("**LOST! **" + ctx.message.author.mention)
            await ctx.send(embed=emb)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def spin(self, ctx: commands.Context):
        s = random.randint(1000, 10000)
        await open_acc(ctx.author)
        await add_bal(ctx.author, s)
        await ctx.channel.send(
            "**You have won `{} INR` .Please check you wallet **".format(s) +
            ctx.message.author.name)

    #---------MINING--------------------#
    @commands.command(pass_context=True)
    async def bag(self, ctx: commands.Context):
        await open_acc(ctx.author)

        member = ctx.author

        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE member_id = {member.id}")
        result = cursor.fetchone()

        embed = discord.Embed(color=get_random_color(),
                              timestamp=ctx.message.created_at)
        embed.set_author(name=f"{member.name}'s Bag",
                         icon_url=member.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Diamonds " + "<a:twitch9100:860049009749000222>",
                        value=f"` {result[4]} `",
                        inline=False)
        embed.add_field(name="Gold " + "<a:twitch29100:860049006750859281>",
                        value=f"` {result[3]} `",
                        inline=False)
        embed.add_field(name="Silver " + "<a:twitch3100:860049006571159552>",
                        value=f"` {result[5]} `",
                        inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}",
                         icon_url=member.avatar_url)

        await ctx.send(embed=embed)

        # start mining

    #21600
    @commands.command(pass_context=True, aliases=['mine'])
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def mining(self, ctx: commands.Context):
        await open_acc(ctx.author)
        member = ctx.author

        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE member_id = {member.id}")
        result = cursor.fetchone()
        db.commit()
        cursor.close()

        await ctx.channel.send("Mining started now ! " +
                               ctx.message.author.name)
        #staff=6 machine=7
        val = result[7]
        if val >= 1:
            await asyncio.sleep(21600 // 2)
            self.mining.reset_cooldown(ctx)
        else:
            await asyncio.sleep(21600)

        staff = result[6]
        if staff == 0:
            d = random.randint(0, 5)
            g = random.randint(5, 20)
            s = random.randint(20, 100)
        else:
            d = random.randint(10, 30)
            g = random.randint(20, 80)
            s = random.randint(100, 200)

        cursor = db.cursor()
        cursor.execute(f"SELECT * from main WHERE member_id = {member.id}")
        result = cursor.fetchone()
        sql = f"UPDATE main SET gold = ?,diamonds = ?,silver = ? WHERE member_id = ?"
        val = (result[3] + g, result[4] + d, result[5] + s, member.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        embed = discord.Embed(title="Mining Completed! ",
                              description=ctx.author.mention,
                              timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Diamonds" + "<a:twitch9100:860049009749000222>",
                        value=f"` {d} `",
                        inline=False)
        embed.add_field(name="Gold" + "<a:twitch29100:860049006750859281>",
                        value=f"` {g} `",
                        inline=False)
        embed.add_field(name="Silver" + "<a:twitch3100:860049006571159552>",
                        value=f"` {s} `",
                        inline=False)

        await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def store(self, ctx: commands.Context):
        await open_acc(ctx.author)
        member = ctx.author
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE member_id = {member.id}")
        result = cursor.fetchone()
        db.commit()
        cursor.close()
        emb = discord.Embed(
            title=ctx.author.name + "'s " + 'Mining store',
            description="Staff : `{}`".format(result[6]) + " \n " +
            "Machine : `{}`\n".format(result[7]) +
            '`upgradeS` :upgrade staff for 50,000 and get 2x mining\n' +
            "`upgradeM` : upgrade machine for 2,00,000 and get mining boost (3hrs)\n"
        )
        await ctx.channel.send(embed=emb)

    @commands.command()
    async def upgradeS(self, ctx: commands.Context):
        await open_acc(user=ctx.author)
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()
        s = result[6]
        if s >= 1:
            await ctx.send("Staff already got upgraded! " + ctx.author.name)
            return
        elif result[2] < 50000:
            await ctx.send("Not enough bank balance! " + ctx.author.name)
            return
        else:
            await remove_bankbal(ctx.author, 50000)
            sql = f"UPDATE main SET staff = ? WHERE member_id = ?"
            val = (1, ctx.author.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send("Successfully upgraded staff! " + ctx.author.name)

    #upgrademachine
    @commands.command()
    async def upgradeM(self, ctx: commands.Context):
        await open_acc(user=ctx.author)
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()
        s = result[7]
        if s >= 1:
            await ctx.send("Machine already got upgraded! " + ctx.author.name)
            return
        elif result[2] < 200000:
            await ctx.send("Not enough bank balance! " + ctx.author.name)
            return
        else:
            await remove_bankbal(ctx.author, 200000)
            sql = f"UPDATE main SET machine = ? WHERE member_id = ?"
            val = (1, ctx.author.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send("Successfully upgraded machine! " + ctx.author.name)

    #upgradestaff
    @commands.command(pass_context=True)
    async def sell(self, ctx: commands.Context, arg, amt):
        await open_acc(user=ctx.author)
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        if amt == "max":
            n1 = int(result[4])
            n2 = int(result[3])
            n3 = int(result[5])

        else:
            n1 = int(amt)
            n2 = int(amt)
            n3 = int(amt)
        if int(amt) <= 0:
            return await ctx.send("Use positive number!")

        d_r = 100
        g_r = 50
        s_r = 10
        await open_acc(user=ctx.author)
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        # diamonds
        if arg.lower() == 'diamonds':
            diamond_count = result[4]
            if diamond_count < n1:
                await ctx.channel.send("Not enough diamonds!")
            elif diamond_count >= n1:
                await add_bankbal(ctx.author, d_r * n1)
                await r_diamonds(ctx.author, n1)
                await ctx.channel.send(
                    "Daimonds has been sold for `{} INR`.Please check your Bank"
                    .format(d_r * n1))
        # Gold
        if arg.lower() == 'gold':
            gold_count = result[3]
            if gold_count < n2:
                await ctx.channel.send("Not enough gold!")
            elif gold_count >= n2:
                await add_bankbal(ctx.author, g_r * n2)
                await r_gold(ctx.author, n2)
                await ctx.channel.send(
                    "Gold has been sold for `{} INR`.Please check your Bank".
                    format(g_r * n2))
        # silver
        if arg.lower() == 'silver':
            silver_count = result[5]
            if silver_count < n3:
                await ctx.channel.send("Not enough silver!")
            elif silver_count >= n3:
                await add_bankbal(ctx.author, s_r * n3)
                await r_silver(ctx.author, n3)

                await ctx.channel.send(
                    "Silver has been sold for `{} INR`.Please check your Bank".
                    format(s_r * n3))

    @commands.command()
    async def vote(self, ctx: commands.Context):
        self.gg_token = ""
        self.bot_id = "844988118637740042"
        self.user_id = ctx.author.id
        self.agent = 'DBL-Python-Library (https://github.com/top-gg/DBL-Python-Library 0.4.0) Python/{0[0]}.{0[' '1]} aiohttp/{1}'.format(
            sys.version_info, aiohttp.__version__)

        headers = {
            'User-Agent': self.agent,
            'Content-Type': 'application/json',
            'Authorization': self.gg_token
        }
        params = {'userId': self.user_id}
        response = requests.get('https://top.gg/api/bots/{}/check'.format(
            self.bot_id),
                                params=params,
                                headers=headers)
        if response.json()['voted'] > 0:
            #await ctx.send("You voted me already! please vote me after every 12 hours "+ctx.author.mention)
            embed = discord.Embed(title=ctx.author.name,
                                  description="Vote me on Top.gg")
            await ctx.send(
                embed=embed,
                components=[  # Use any button style you wish to :)
                    [
                        Button(
                            label="Vote",
                            style=ButtonStyle.URL,
                            url="https://top.gg/bot/844988118637740042/vote")
                    ]
                ])
        else:
            embed = discord.Embed(title="Vote me!",
                                  description="Vote me on Top.gg")
            await ctx.send(
                embed=embed,
                components=[  # Use any button style you wish to :)
                    [
                        Button(
                            label="Vote",
                            style=ButtonStyle.URL,
                            url="https://top.gg/bot/844988118637740042/vote")
                    ]
                ])


def setup(client):
    client.add_cog(Bank(client))
