import asyncio

from discord.ext import commands
import discord
import datetime
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


# --------------------------------HELP PAGES-----------------------------#
async def home_page():
    embedVar = discord.Embed(
        title="Command prefix : `p!`  or `mention me`\n",
        description="<a:dc9100:860589083938783254>" + " **Misc - 10 : **\n" +
        "`user`" + "," + "`avatar`" + "," + "`btc`" + "," + "`ping`" + "," +
        "`timer <seconds>`" + "," + "`clear <amount>`" + "," + "`uptime`" +
        "," + "`vote`" + "\n\n" + "<a:bank9100:871463087415369838>" +
        " **Bank - 4 : **\n" + "`bal`" + "," + "`withdraw <amount>`" + "," +
        "`dep <amount>`" + "," + "`send <mention> <amount>`" + "\n\n" +
        "<a:admin9100:872740437893468180>" + " **Admin - 3 : **\n" +
        "`welcome`" + "," + "`leave`" + "," + "`reset`"  #+ "," + "`lockdown`"
        + "\n\n" + "<a:economy9100:860587342556037130>" +
        " **Economy - 2 : **\n" + "`spin`" + "," + "`tada <amount>`" + "\n\n" +
        "<a:hammer9100:860049001960964126>" + " **Mining - 4 : **\n" +
        "`bag`" + "," + "`mining`" + "," + "`store`" + "," +
        "`sell <variant> <value>`" + "\n\n" +
        "<a:info9100:873577144016592908>" + " **Info - 4 : **\n" + "`phn`" +
        "," + "`serverinfo`" + "," + "`botinfo`" + "\n\n" +
        "<a:warn9100:860049001717825548>" + " **Mod - 7 : **\n" + "`kick`" +
        "," + "`role`" + "," + "`mute`" + "," + "`unmute`" + "," + "`ban`" +
        "," + "`unban`" + "," + "`banlist`" + "\n\n" +
        "[invite](https://discord.com/api/oauth2/authorize?client_id=844988118637740042&permissions=8&scope=bot)"
        + " | " + "[support](https://discord.gg/PxYxjA8uDy)\n\n",
        color=0xFF5733,
        timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/iPItsO8.gif")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')

    return embedVar


async def sample_page():
    embedVar = discord.Embed(
        title="<a:dc9100:860589083938783254>" + " Misc",
        description="`user <mention>` - user information\n" +
        "`avatar` - author avatar\n" +
        "`btc <currency>` - btc price (default:USD)\n" +
        "`ping` - bot latency\n" +
        "`timer <sec>` - set timer range(1-300s)\n" +
        "`clear <amount>` - clear messages\n" + "`vote` - vote me on Top.gg" +
        "\n`uptime` - bot uptime" + "\n\n",
        color=0xFF5733,
        timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/iPItsO8.gif")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')

    return embedVar


async def bank_page():
    embedVar = discord.Embed(title="<a:bank9100:871463087415369838>" + " Bank",
                             description="`bal` - check bank balance\n" +
                             "`withdraw <amount>` - withdraw to wallet\n" +
                             "`dep <amount>` - depost money in bank\n" +
                             "`send <mention> <amount>` - send money\n" + "\n",
                             color=0xFF5733,
                             timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/iPItsO8.gif")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')
    return embedVar


async def economy_page():
    embedVar = discord.Embed(title="<a:economy9100:860587342556037130>" +
                             " Economy",
                             description="`spin` - daily reward\n" +
                             "`tada <amount>` - simple game" + "\n\n",
                             color=0xFF5733,
                             timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/iPItsO8.gif")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')
    return embedVar


async def mining_page():
    embedVar = discord.Embed(
        title="<a:hammer9100:860049001960964126>" + " Mining",
        description="`bag` - assests\n" +
        "`mining` - start mining (Max : 6hrs)\n" + "`store` - buy assests\n" +
        "`sell <variant> <amount>` - sell assests" + "\n\n",
        color=0xFF5733,
        timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/iPItsO8.gif")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')
    return embedVar


async def mod_page():
    embedVar = discord.Embed(
        title="<a:warn9100:860049001717825548>" + " Mod",
        description="`kick` - kick user from server\n" +
        "`mute` - mute user\n" + "`unmute` - unmute user\n" +
        "`ban` - ban user from server\n" +
        "`banlist` - List of banned members\n" +
        "`role <@member> <@role>` - mute user\n" + "`unban` - unban user" +
        "\n\n",
        color=0xFF5733,
        timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/iPItsO8.gif")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')
    return embedVar


async def admin_page():
    embedVar = discord.Embed(
        title="<a:admin9100:872740437893468180>" + " Admin",
        description="`need manage server permission`\n\n" +
        "`logs <limit>` - server logs \n" +
        "`welcome <channel_id>` - welcome users in channel with card\n" +
        "`leave <channel_id>` - say goodbye in channel\n" +
        "`reset` - reset welcome and leave setup" + "\n\n" +
        "`Tip:` - right click on channel to copy channel id" + "\n\n",
        color=0xFF5733,
        timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/iPItsO8.gif")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')
    return embedVar


async def info_page():
    embedVar = discord.Embed(
        title="<a:info9100:873577144016592908>" + " INFO",
        description=
        "`phn <number_with_countrycode>` - send this in bot dm to know number details \n"
        + "`serverinfo` - server information\n" +
        "`botinfo` - Bot information\n" + "\n\n",
        color=0xFF5733,
        timestamp=datetime.datetime.utcnow())
    embedVar.set_image(url="https://i.imgur.com/iPItsO8.gif")
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text="Thanks for using priya bot " + '\u200b')
    return embedVar


class Help(commands.Cog):
    """Returns random results"""
    def __init__(self, client):
        self.client = client
        DiscordComponents(client)

    # -----------------------multi help page------------------------------#

    @commands.command()
    async def help(self, ctx: commands.context):
        # Sets a default embed
        current = 0
        hm_page = await home_page()
        sm_page = await sample_page()
        b_page = await bank_page()
        e_page = await economy_page()
        m_page = await mining_page()
        md_page = await mod_page()
        ad_page = await admin_page()
        i_page = await info_page()
        paginationList = [
            hm_page, sm_page, b_page, ad_page, e_page, m_page, md_page, i_page
        ]
        # Sending first message
        # I used ctx.reply, you can use simply send as well
        mainMessage = await ctx.send(
            "HELP MENU",
            embed=paginationList[current],
            components=[  # Use any button style you wish to :)
                [
                    Button(label="Prev", id="back", style=ButtonStyle.green),
                    Button(
                        label=
                        f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                        id="cur",
                        style=ButtonStyle.grey,
                        disabled=True),
                    Button(label="Next", id="front", style=ButtonStyle.green)
                ]
            ])
        # Infinite loop
        while True:

            def check(m):
                m.user = ctx.author

            # Try and except blocks to catch timeout and break
            try:
                interaction = await self.client.wait_for(
                    "button_click",
                    check=lambda i: i.component.id in ["back", "front"] and
                    check,  # You can add more
                    timeout=30.0)

                # Getting the right list index
                if interaction.component.id == "back" and interaction.user == ctx.author:
                    current -= 1
                elif interaction.component.id == "front" and interaction.user == ctx.author:
                    current += 1
                # If its out of index, go back to start / end
                if current == len(paginationList):
                    current = 0
                elif current < 0:
                    current = len(paginationList) - 1

                # Edit to new page + the center counter changes
                await interaction.respond(
                    type=InteractionType.UpdateMessage,
                    embed=paginationList[current],
                    components=[  # Use any button style you wish to :)
                        [
                            Button(label="Prev",
                                   id="back",
                                   style=ButtonStyle.green),
                            Button(
                                label=
                                f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                                id="cur",
                                style=ButtonStyle.grey,
                                disabled=True),
                            Button(label="Next",
                                   id="front",
                                   style=ButtonStyle.green)
                        ]
                    ])
            except asyncio.TimeoutError:
                # Disable and get outta here
                await mainMessage.edit(components=[[
                    Button(label="Prev",
                           id="back",
                           style=ButtonStyle.red,
                           disabled=True),
                    Button(
                        label=
                        f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                        id="cur",
                        style=ButtonStyle.grey,
                        disabled=True),
                    Button(label="Next",
                           id="front",
                           style=ButtonStyle.red,
                           disabled=True)
                ]])
                break


def setup(client):
    client.add_cog(Help(client))
