import asyncio

from discord.ext import commands
import random
import discord
import datetime


# --------------------------------HELP PAGES-----------------------------#
async def home_page():
    embedVar = discord.Embed(
        title="Command prefix : `p!`\n",
        description="**Misc - 6 : **\n" + "`id`" + "," + "`avatar`" + "," +
        "`btc`" + "," + "`ping`" + "," + "`timer <seconds>`" + "," +
        "`clear <amount>`" + "," + "`uptime`" + "\n\n" + "**Bank - 4 : **\n" +
        "`bal`" + "," + "`withdraw <amount>`" + "," + "`dep <amount>`" + "," +
        "`send <mention> <amount>`" + "\n\n" + "**Economy - 2 : **\n" +
        "`spin`" + "," + "`tada <amount>`" + "\n\n" + "**Mining - 3 : **\n" +
        "`bag`" + "," + "`mining`" + "," + "`store`" + "," +
        "`sell <variant> <value>`" + "\n\n"
        # "<a:rainbowline:860049001860038677>"
        +
        "[invite](https://discord.com/api/oauth2/authorize?client_id=844988118637740042&permissions=8&scope=bot)\n\n",
        color=0xFF5733,
        timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/WDSmWA0.jpg")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')

    return embedVar


async def sample_page():
    embedVar = discord.Embed(
        title="Misc",
        description="`id` - author id\n" + "`avatar` - author avatar\n" +
        "`btc` - btc rate in INR\n" + "`ping` - bot latency\n" +
        "`timer <sec>` - set timer range(1-300s)\n" +
        "`clear <amount>` - clear messages" + "\n`uptime` - bot uptime" +
        "\n\n",
        color=0xFF5733,
        timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/WDSmWA0.jpg")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')

    return embedVar


async def bank_page():
    embedVar = discord.Embed(title="Bank",
                             description="`bal` - check bank balance\n" +
                             "`withdraw <amount>` - withdraw to wallet\n" +
                             "`dep <amount>` - depost money in bank\n" +
                             "`send <mention> <amount>` - send money\n" + "\n",
                             color=0xFF5733,
                             timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/WDSmWA0.jpg")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')
    return embedVar


async def economy_page():
    embedVar = discord.Embed(title="Economy",
                             description="`spin` - daily reward\n" +
                             "`tada <amount>` - simple game" + "\n\n",
                             color=0xFF5733,
                             timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/WDSmWA0.jpg")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')
    return embedVar


async def mining_page():
    embedVar = discord.Embed(
        title="Mining",
        description="`bag` - assests\n" +
        "`mining` - start mining (Max : 6hrs)\n" + "`store` - buy assests\n" +
        "`sell <variant> <amount>` - sell assests" + "\n\n",
        color=0xFF5733,
        timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/WDSmWA0.jpg")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')
    return embedVar


class Help(commands.Cog):
    """Returns random results"""
    def __init__(self, client):
        self.client = client

    # -----------------------multi help page------------------------------#

    @commands.command()
    async def help1(self, ctx: commands.Context):
        contents = ["home", "Misc", "Economy!", "Bank!", "Mining!"]
        pages = 5
        cur_page = 1

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [
                "<a:arrright:859808773912395776>",
                "<a:downleft:859808771122397235>"
            ]

        hm_page = await home_page()
        firs_page = await sample_page()
        second_page = await economy_page()
        third_page = await bank_page()
        fourth_page = await mining_page()

        if cur_page == 1:
            message = await ctx.send(
                content="<a:bluetick:859677933822804019>" +
                f"**Page : {cur_page}/{pages}: **",
                embed=hm_page)
        await message.add_reaction("<a:downleft:859808771122397235>")
        await message.add_reaction("<a:arrright:859808773912395776>")

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add",
                                                            timeout=60,
                                                            check=check)
                if str(
                        reaction.emoji
                ) == "<a:arrright:859808773912395776>" and cur_page != pages:
                    cur_page += 1
                    if cur_page == 1:
                        await message.edit(
                            content="<a:bluetick:859677933822804019>" +
                            f"Page {cur_page}/{pages}: ",
                            embed=hm_page)
                    elif cur_page == 2:
                        await message.edit(
                            content="<a:bluetick:859677933822804019>" +
                            f"Page {cur_page}/{pages}: ",
                            embed=firs_page)
                    elif cur_page == 3:
                        await message.edit(
                            content="<a:bluetick:859677933822804019>" +
                            f"Page {cur_page}/{pages}: ",
                            embed=second_page)
                    elif cur_page == 4:
                        await message.edit(
                            content="<a:bluetick:859677933822804019>" +
                            f"Page {cur_page}/{pages}: ",
                            embed=third_page)
                    elif cur_page == 5:
                        await message.edit(
                            content="<a:bluetick:859677933822804019>" +
                            f"Page {cur_page}/{pages}: ",
                            embed=fourth_page)

                    # await message.edit(embed=firs_page)  #(content=f"Help Book {cur_page}/{pages}:\n{contents[cur_page-1]}")
                    await message.remove_reaction(reaction, user)
                elif str(
                        reaction.emoji
                ) == "<a:downleft:859808771122397235>" and cur_page > 1:
                    cur_page -= 1
                    if cur_page == 1:
                        await message.edit(
                            content="<a:bluetick:859677933822804019>" +
                            f"Page {cur_page}/{pages}: ",
                            embed=hm_page)
                    elif cur_page == 2:
                        await message.edit(
                            content="<a:bluetick:859677933822804019>" +
                            f"Page {cur_page}/{pages}: ",
                            embed=firs_page)
                    elif cur_page == 3:
                        await message.edit(
                            content="<a:bluetick:859677933822804019>" +
                            f"Page {cur_page}/{pages}: ",
                            embed=second_page)
                    elif cur_page == 4:
                        await message.edit(
                            content="<a:bluetick:859677933822804019>" +
                            f"Page {cur_page}/{pages}: ",
                            embed=third_page)
                    elif cur_page == 5:
                        await message.edit(
                            content="<a:bluetick:859677933822804019>" +
                            f"Page {cur_page}/{pages}: ",
                            embed=fourth_page)
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

    @commands.command()
    async def help(self, ctx: commands.context):
        hm_page = await home_page()
        await ctx.channel.send(embed=hm_page)


def setup(client):
    client.add_cog(Help(client))
