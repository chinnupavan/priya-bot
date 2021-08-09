import asyncio
from discord.ext import commands
from discord_components import *

import discord
class Misc(commands.Cog):
    """Returns random results"""

    def __init__(self, client):
        self.client=client
        DiscordComponents(client)

    @commands.command()
    async def ping(self,ctx:commands.Context):
        pembedVar = discord.Embed(
            description="<a:ping9100:859882795651825695>" + " Latency  " + f"```{round(self.client.latency * 1000)} ms```"
            ,
            color=0xFF5733)
        await ctx.send(embed=pembedVar)

    @commands.command()
    async def user(self,ctx:commands.Context, userinfo: discord.Member = None):
        if userinfo==None:
            author=ctx.author
        else:
            author=userinfo
        em = discord.Embed(title="INFO : ")
        em.set_author(name=f"{author.name}#{author.discriminator}",
                                     icon_url=author.avatar_url)
        em.set_thumbnail(url=author.avatar_url)
        em.add_field(name="Name", value=f"{author.name}#{author.discriminator}",
                                    inline=False)
        em.add_field(name="Nickname", value=f"{author.nick}",
                                    inline=False)
        em.add_field(name="id", value=f"{author.id}", inline=False)
        em.add_field(name="Account creation", value=f"{author.created_at}",
                                    inline=False)
        await ctx.send(embed=em)

    @commands.command()
    async def botinfo(self,ctx:commands.Context):
        author = ctx.author
        bot = self.client.user
        botId = self.client.user.id
        botIcon = self.client.user.avatar_url
        servers = self.client.guilds
        users = 0
        for g in self.client.guilds:
            for i in g.members:
                users=users+1
        botinfoEmbed = discord.Embed(title="INFO : ")
        botinfoEmbed.set_author(name=f"{author.name}#{author.discriminator}",
                                icon_url=author.avatar_url)
        botinfoEmbed.set_thumbnail(url=botIcon)
        botinfoEmbed.add_field(name="Name : ", value=f"` {bot.name}#{bot.discriminator}    `",inline=False)
        botinfoEmbed.add_field(name="Id : ", value=f"` {botId}  `", inline=False)
        botinfoEmbed.add_field(name="Servers : ", value=f"` {len(servers)}  `", inline=False)
        botinfoEmbed.add_field(name="Members : ", value=f"` {users}  `", inline=False)
        botinfoEmbed.add_field(name="Library : ", value="` discord.py 1.7.3    `", inline=False)
        botinfoEmbed.add_field(name="Created by ", value="` GhostKiller#4676    `",inline=False)

        x = ctx.guild.created_at.now()
        botinfoEmbed.add_field(name="Created At", value=f"`{x.year}-{x.month}-{x.day}` `{x.hour}hrs {x.minute}min {x.second}sec`", inline=False)


        components=[
            Button(
                   style=ButtonStyle.URL,
                   label="Invite",
                   url="https://www.google.com"
                   )
            ]
        u="https://discord.com/api/oauth2/authorize?client_id=844988118637740042&permissions=261993005047&scope=bot"
        await ctx.send(embed=botinfoEmbed,components=[
            Button(
                   style=ButtonStyle.URL,
                   label="Invite",
                   url=u
                   ),
            Button(
                style=ButtonStyle.URL,
                label="Support server",
                url="https://discord.gg/ax6zhRq8CD"
            )
            ])
    # timer
    @commands.command()
    async def timer(self,ctx:commands.Context, seconds):
        try:
            secondint = int(seconds)
            if secondint < 1 or secondint > 300:
                embedVar = discord.Embed(
                    description="<a:timer9100:859871243054481438>" + " : " + " please use range between 1-300s"
                    ,
                    color=0xFF5733)
                await ctx.send(embed=embedVar)
            else:

                embedVar = discord.Embed(
                    description="<a:timer9100:859871243054481438>" + " Remaining : " + f"{seconds}"
                    ,
                    color=0xFF5733)

                message = await ctx.send(embed=embedVar)
                await asyncio.sleep(1)
                for i in range(secondint - 1, -1, -1):
                    embedVar = discord.Embed(
                        description="<a:timer9100:859871243054481438>" + " Remaining : " + f"{i}",
                        color=0xFF5733)
                    await message.edit(embed=embedVar)
                    await asyncio.sleep(1)
                await message.delete()
                embedVar = discord.Embed(
                    description="<a:timer9100:859871243054481438>" + " : " + ctx.author.mention + " Your countdown " + f"{seconds}s " + "Has ended!",
                    color=0xFF5733)
                await ctx.send(embed=embedVar)

        except ValueError:
            embedVar = discord.Embed(description="<a:timer9100:859871243054481438>" + " Must be a number!",
                                     color=0xFF5733)
            await ctx.send(embed=embedVar)


    @commands.command()
    async def avatar(self,ctx:commands.Context,member:discord.member=None):
        embedd = discord.Embed(title=ctx.author.name, colour=0x0DDCFF)
        if member==None:
            embedd.set_image(
                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=128".format(ctx.author))
        else:
            embedd.set_image(
                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=128".format(member))
        await ctx.send(embed=embedd)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx:commands.Context, args: int):
        s = int(args)
        dele = await ctx.channel.purge(limit=s)
        emd = discord.Embed(description=f"{len(dele):,} messages have been deleted.")
        await ctx.channel.send(embed=emd, delete_after=3)

    @commands.command()
    @commands.bot_has_permissions(manage_guild=True)
    async def serverinfo(self,ctx:commands.Context):
        guild=ctx.guild
        emb=discord.Embed(Title="Server Info",description=guild.description ,colour=0xedab5f)
        emb.add_field(name="Server ID", value=f"`{guild.id}`",inline=False)
        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        emb.set_thumbnail(url=guild.icon_url)
        emb.add_field(name="Members", value=f"`{guild.member_count}`", inline=True)
        emb.add_field(name="Channels", value=f"`{len(guild.channels)}`", inline=True)
        emb.add_field(name="Voice channels", value=f"`{len(guild.voice_channels)}`", inline=False)
        emb.add_field(name="Text channels", value=f"`{len(guild.text_channels)}`", inline=True)
        emb.add_field(name="Roles", value=f"`{len(guild.roles)}`", inline=True)
        emb.add_field(name="Emojis", value=f"`{len(guild.emojis)}`", inline=True)
        emb.add_field(name="Verification level", value=f"`{guild.verification_level}`", inline=True)
        emb.add_field(name="Region", value=f"`{guild.region}`", inline=True)
        x=guild.created_at.now()
        emb.add_field(name="Created At", value=f"`{x.year}-{x.month}-{x.day}` `{x.hour}hrs {x.minute}min {x.second}sec`", inline=False)


        await ctx.send(embed=emb)

    @commands.command()
    @commands.bot_has_permissions(manage_guild=True)
    async def logs(self,ctx:commands.Context,amt=None):
        if amt==None:
            await ctx.send("please specify limit `logs <limit>`")
        a=int(amt)
        c=1
        embed=discord.Embed(title="Audit Logs")
        async for entry in ctx.guild.audit_logs(limit=a):
            #embed.add_field(name=" ",value=f"{entry.user} {entry.action } {entry.target}")
            embed.add_field(name=c,value='`{0.user} did {0.action} to {0.target}`'.format(entry),inline=False)
            c+=1
            #await ctx.send('`{0.user} did {0.action} to {0.target}`'.format(entry))
        await ctx.send(embed=embed)







def setup(client):
    client.add_cog(Misc(client))