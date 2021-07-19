#Thanks to https://github.com/AHiddenDonut/Economy-Bot-Youtube for databse tutorial

import asyncio
import json

from discord.ext import commands
import random
import discord
import sqlite3


async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)

    return users


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


async def mc(user):
    users = await get_bank_data()
    p = users[str(user.id)]["machine"]
    i = int(p)
    if i > 0:
        return 21600 // 2
    return 21600


# update bank details


class Bank(commands.Cog):
    """Returns random results"""
    def __init__(self, client):
        self.client = client

#----------------------------Bank--------------------------#

    @commands.command()
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
        embed.add_field(name="Wallet", value=f"{result[1]} ")
        embed.add_field(name="Bank", value=f"{result[2]} ")
        embed.set_footer(text=f"Requested by {ctx.author}",
                         icon_url=member.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    #wallet=1 bank=2
    @commands.command(name="dep", aliases=['deposit'])
    async def dep(self, ctx: commands.context, amount=None):
        await open_acc(user=ctx.author)
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        if result[1] == 0:
            return await ctx.send("Low balance!")
        if str(amount) == "max":
            sql = "UPDATE main SET bank = ? WHERE member_id = ?"
            val = (result[2] + result[1], ctx.author.id)
            await ctx.send(f"Successfully deposited **{result[1]}**")
            await remove_bal(ctx.author, result[1])
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

            await ctx.send(f"Successfully deposited f{amount}!")

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
        if result[2] == 0:
            return await ctx.send("Low balance")
        if amount == "max":
            sql = "UPDATE main SET bank = ? WHERE member_id = ?"
            val = (0, ctx.author.id)
            await add_bal(ctx.author, result[2])
            await remove_bankbal(ctx.author, result[2])
            await ctx.send(f"You successfully withdrawn **{result[2]}** ")

        if int(amount) >= 1:
            amt = int(amount)

            if amt >= result[2]:
                sql = "UPDATE main SET bank = ? WHERE member_id = ?"
                val = (0, ctx.author.id)
                await add_bal(ctx.author, result[2])
                await ctx.send(f"You successfully withdrawn **{result[2]}**")
            else:
                sql = "UPDATE main SET bank = ? WHERE member_id = ?"
                val = (result[2] - amount, ctx.author.id)
                await add_bal(ctx.author, amount)
                await ctx.send(f"You successfully withdrawn **{amount}**")

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.command()
    async def send(self,
                   ctx: commands.context,
                   member: discord.Member = None,
                   amount=None):
        if member == None:
            await ctx.send(
                "Please mention user whom you want to transfer money!")
        else:
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
                           ctx.message.author.mention)
            return
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
                                ctx.message.author.mention + "\n\n" + "[ " +
                                s1 + " , " + s2 + " , " + s3 + " ]\n")
            # await ctx.send("**WON! **" + ctx.message.author.mention)
            await ctx.send(embed=emb)
        else:
            await remove_bal(ctx.author, int(amount))
            emb = discord.Embed(description="**Lost!**    " +
                                ctx.message.author.mention + "\n\n" + "[ " +
                                s1 + " , " + s2 + " , " + s3 + " ]\n")
            # await ctx.send("**LOST! **" + ctx.message.author.mention)
            await ctx.send(embed=emb)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def spin(self, ctx: commands.Context):
        s = random.randint(100, 1000)
        await open_acc(ctx.author)
        await add_bal(ctx.author, s)
        await ctx.channel.send(
            "**You have won {} .Please check you wallet **".format(s) +
            ctx.message.author.mention)


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
        embed.add_field(name="Gold", value=f"{result[3]} ")
        embed.add_field(name="Diamonds", value=f"{result[4]} ")
        embed.add_field(name="Silver", value=f"{result[5]} ")
        embed.set_footer(text=f"Requested by {ctx.author}",
                         icon_url=member.avatar_url)

        await ctx.send(embed=embed)

        # start mining

    @commands.command(pass_context=True)
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
                               ctx.message.author.mention)

        val = result[6]
        if val >= 1:
            await asyncio.sleep(21600 // 2)
            self.mining.reset_cooldown(ctx)
        else:
            await asyncio.sleep(21600)

        staff = result[5]
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
        await ctx.channel.send(
            ctx.author.mention +
            "\nYour mining has done! you got\n`Diamonds :{0}`\n`Gold :{1}`\n`Silver :{2}`"
            .format(d, g, s))

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
            title='Mining store',
            description="Your staff : `{}`".format(result[6]) + " , " +
            "Your Machine : `{}`\n".format(result[7]) +
            '`upgrade staff` :upgrade staff for 50,000 and get 2x mining\n' +
            "`upgrade machine` : upgrade machine for 2,00,000 and get mining boost (3hrs)\n"
        )
        await ctx.channel.send(embed=emb)

    @commands.command(pass_context=True)
    async def sell(self, ctx: commands.Context, arg, amt):
        await open_acc(user=ctx.author)
        db = sqlite3.connect('bank.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()
        if str(arg) == "max":
            return await ctx.send("comming soon")

        n = int(amt)
        if n <= 0:
            return await ctx.send("please sell more than 1 items!")

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
            if diamond_count < n:
                await ctx.channel.send("Not enough diamonds!")
            elif diamond_count >= n:
                await add_bankbal(ctx.author, d_r * n)
                await r_diamonds(ctx.author, n)
                await ctx.channel.send(
                    "Daimonds has been sold for {}.Please check your Bank".
                    format(d_r * n))
        # Gold
        if arg.lower() == 'gold':
            gold_count = result[3]
            if gold_count < n:
                await ctx.channel.send("Not enough gold!")
            elif gold_count >= n:
                await add_bankbal(ctx.author, g_r * n)
                await r_gold(ctx.author, n)
                await ctx.channel.send(
                    "Gold has been sold for {}.Please check your Bank".format(
                        g_r * n))
        # silver
        if arg.lower() == 'silver':
            silver_count = result[5]
            if silver_count < n:
                await ctx.channel.send("Not enough silver!")
            elif silver_count >= n:
                await add_bankbal(ctx.author, s_r * n)
                await r_silver(ctx.author, n)

                await ctx.channel.send(
                    "Silver has been sold for {}.Please check your Bank".
                    format(s_r * n))


def setup(client):
    client.add_cog(Bank(client))
