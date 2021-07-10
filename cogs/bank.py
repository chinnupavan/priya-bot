import asyncio
import json

from discord.ext import commands
import random
import discord


async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)

    return users


# opens an account
async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 200000
        users[str(user.id)]["diamonds"] = 0
        users[str(user.id)]["gold"] = 0
        users[str(user.id)]["silver"] = 0
        users[str(user.id)]["staff"] = 0
        users[str(user.id)]["machine"] = 0

    with open("bank.json", "w") as f:
        json.dump(users, f)
    return True

    # returns json file details


async def mc(user):
    users = await get_bank_data()
    p = users[str(user.id)]["machine"]
    i = int(p)
    if i > 0:
        return 21600 // 2
    return 21600


# update bank details
async def update_bank(user, change=0, mode='wallet'):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("bank.json", "w") as f:
        json.dump(users, f)
    bal = users[str(user.id)]["wallet"], users[str(user.id)]["bank"], users[str(user.id)]["diamonds"], \
            users[str(user.id)]["gold"], users[str(user.id)]["silver"]
    return bal


class Bank(commands.Cog):
    """Returns random results"""
    def __init__(self, client):
        self.client = client

#----------------------------Bank--------------------------#

    @commands.command(pass_context=True)
    async def bal(self, ctx: commands.Context):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()
        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        embed = discord.Embed(title=f"{ctx.author.name}'s balance",
                              color=0xFF69B4)
        embed.add_field(name="Bank : ", value=bank_amt, inline=False)
        embed.add_field(name="Wallet : ", value=wallet_amt, inline=False)
        await ctx.send(embed=embed)

    # withdraw
    @commands.command(pass_context=True)
    async def withdraw(self, ctx: commands.Context, amount=None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please use withdraw <amount> " +
                           ctx.message.author.mention)
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send("**Low balance! **" + ctx.message.author.mention)
            return
        if amount < 0:
            await ctx.send("**Use positive number **" +
                           ctx.message.author.mention)
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")

        await ctx.send(f"**Done! Added {amount} to wallet! **" +
                       ctx.message.author.mention)

    # dep
    @commands.command(pass_context=True)
    async def dep(self, ctx: commands.Context, amount=None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please use withdraw <amount> " +
                           ctx.message.author.mention)
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[0]:
            await ctx.send("**Low balance! **" + ctx.message.author.mention)
            return
        if amount < 0:
            await ctx.send("**Use positive number **" +
                           ctx.message.author.mention)
            return

        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, "bank")

        await ctx.send(f"**Done! Deposited {amount}!** " +
                       ctx.message.author.mention)

    # transfer
    @commands.command(pass_context=True)
    async def send(self,
                   ctx: commands.Context,
                   member: discord.Member,
                   amount=None):
        await open_account(ctx.author)
        await open_account(member)
        if amount == None:
            await ctx.send("**please use send <mention_user> <amount> **" +
                           ctx.message.author.mention)
            return

        bal = await update_bank(ctx.author)

        if amount == "all":
            amount = bal[0]

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send("**Low balance! **" + ctx.message.author.mention)
            return
        if amount < 0:
            await ctx.send("**use positive number** " +
                           ctx.message.author.mention)
            return

        await update_bank(ctx.author, -1 * amount, "bank")
        await update_bank(member, amount, "bank")

        await ctx.send(f"**You just sent {amount}!** " +
                       ctx.message.author.mention)

#---------------------------- GAMES -----------------------------#

# spin(daily 4 rewards) and cool down(6 hrs=21600s)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def spin(self, ctx: commands.Context):
        s = random.randint(100, 1000)
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()
        earnings = s
        users[str(user.id)]["wallet"] += earnings
        with open("bank.json", "w") as f:
            json.dump(users, f)
        await ctx.channel.send(
            "**You have won {} .Please check you wallet **".format(s) +
            ctx.message.author.mention)

    # tada game (if two emojis matches out of three you may win)
    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def tada(self, ctx: commands.Context, amount=None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("use format tada <amount> " +
                           ctx.message.author.mention)
            return
        bal = await update_bank(ctx.author)
        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("low balance!" + ctx.message.author.mention)
            return
        if amount < 0:
            await ctx.send("use positive number")
            return
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

        #await ctx.send(str(final[0]," ",final(1)))

        if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
            await update_bank(ctx.author, 1 * amount)
            emb = discord.Embed(description="**Won!**    " +
                                ctx.message.author.mention + "\n\n" + "[ " +
                                s1 + " , " + s2 + " , " + s3 + " ]\n")
            #await ctx.send("**WON! **" + ctx.message.author.mention)
            await ctx.send(embed=emb)
        else:
            await update_bank(ctx.author, -1 * amount)
            emb = discord.Embed(description="**Lost!**    " +
                                ctx.message.author.mention + "\n\n" + "[ " +
                                s1 + " , " + s2 + " , " + s3 + " ]\n")
            #await ctx.send("**LOST! **" + ctx.message.author.mention)
            await ctx.send(embed=emb)


#----------------------------------MINING----------------------#

    @commands.command(pass_context=True)
    async def bag(self, ctx: commands.Context):
        await open_account(ctx.author)

        user = ctx.author

        users = await get_bank_data()
        diam_amt = users[str(user.id)]["diamonds"]
        gold_amt = users[str(user.id)]["gold"]
        silver_amt = users[str(user.id)]["silver"]
        embed = discord.Embed(title=f"{ctx.author.name}'s Bag", color=0xFF69B4)
        embed.add_field(name="Diamonds : ", value=diam_amt, inline=False)
        embed.add_field(name="Gold : ", value=gold_amt, inline=True)
        embed.add_field(name="Silver : ", value=silver_amt, inline=True)

        await ctx.send(embed=embed)

    # start mining
    @commands.command(pass_context=True)
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def mining(self, ctx: commands.Context):
        await ctx.channel.send("Mining started now ! " +
                               ctx.message.author.mention)
        users = await get_bank_data()
        val = users[str(ctx.author.id)]["machine"]
        if val >= 1:
            await asyncio.sleep(21600 // 2)
            self.mining.reset_cooldown(ctx)
        else:
            await asyncio.sleep(21600)
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()
        staff = users[str(user.id)]["staff"]
        if staff == 0:
            d = random.randint(0, 5)
            g = random.randint(5, 20)
            s = random.randint(20, 100)
        else:
            d = random.randint(10, 30)
            g = random.randint(20, 80)
            s = random.randint(100, 200)

        users[str(user.id)]["diamonds"] += d
        users[str(user.id)]["gold"] += g
        users[str(user.id)]["silver"] += s

        await ctx.channel.send(
            ctx.author.mention +
            "\nYour mining has done! you got\n`Diamonds :{0}`\n`Gold :{1}`\n`Silver :{2}`"
            .format(d, g, s))

        with open("bank.json", "w") as f:
            json.dump(users, f)

    # sell mining stuff
    @commands.command(pass_context=True)
    async def sell(self, ctx: commands.Context, arg, amt):
        n = int(amt)
        d_r = 100
        g_r = 50
        s_r = 10
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        # diamonds
        if arg.lower() == 'diamonds':
            diamond_count = users[str(user.id)]["diamonds"]
            if diamond_count < n:
                await ctx.channel.send("Not enough diamonds!")
            elif diamond_count >= n:
                users[str(user.id)]["bank"] += d_r * n
                users[str(user.id)]["diamonds"] -= n
                await ctx.channel.send(
                    "Daimonds has been sold for {}.Please check your Bank".
                    format(d_r * n))
        # Gold
        if arg.lower() == 'gold':
            gold_count = users[str(user.id)]["gold"]
            if gold_count < n:
                await ctx.channel.send("Not enough gold!")
            elif gold_count >= n:
                users[str(user.id)]["bank"] += g_r * n
                users[str(user.id)]["gold"] -= n
                await ctx.channel.send(
                    "Gold has been sold for {}.Please check your Bank".format(
                        g_r * n))
        # silver
        if arg.lower() == 'silver':
            silver_count = users[str(user.id)]["silver"]
            if silver_count < n:
                await ctx.channel.send("Not enough silver!")
            elif silver_count >= n:
                users[str(user.id)]["bank"] += s_r * n
                users[str(user.id)]["silver"] -= n
                await ctx.channel.send(
                    "Silver has been sold for {}.Please check your Bank".
                    format(s_r * n))

        with open("bank.json", "w") as f:
            json.dump(users, f)

    # buy mining boosts
    @commands.command(pass_context=True)
    async def upgrade(self, ctx: commands.Context, args):
        if args.lower() != "staff" and args.lower() != "machine":
            await ctx.channel.send("please visit store :'`store`'")
        else:
            await open_account(ctx.author)
            user = ctx.author
            users = await get_bank_data()
            balance = users[str(user.id)]["bank"]
            if args.lower() == "staff":
                if balance < 50000:
                    await ctx.channel.send("Your bank balance is low! " +
                                           ctx.message.author.mention)
                else:
                    users[str(user.id)]["staff"] += 1
                    users[str(user.id)]["bank"] -= 50000
                    await ctx.channel.send("Upgraded staff! " +
                                           ctx.message.author.mention)

            elif args.lower() == "machine":
                if balance < 100000:
                    await ctx.channel.send("Your bank balance is low! " +
                                           ctx.message.author.mention)
                else:
                    users[str(user.id)]["machine"] += 1
                    users[str(user.id)]["bank"] -= 100000
                    await ctx.channel.send("Upgraded Machine! " +
                                           ctx.message.author.mention)

            with open("bank.json", "w") as f:
                json.dump(users, f)

    # store
    @commands.command(pass_context=True)
    async def store(self, ctx: commands.Context):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        stf = users[str(user.id)]["staff"]
        mach = users[str(user.id)]["machine"]

        emb = discord.Embed(
            title='Mining store',
            description="Your staff : `{}`".format(stf) + " , " +
            "Your Machine : `{}`\n".format(mach) +
            '`upgrade staff` :upgrade staff for 50,000 and get 2x mining\n' +
            "`upgrade machine` : upgrade machine for 2,00,000 and get mining boost (3hrs)\n"
        )
        await ctx.channel.send(embed=emb)


def setup(client):
    client.add_cog(Bank(client))
