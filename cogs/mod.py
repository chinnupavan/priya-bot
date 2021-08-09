import asyncio
import os
from asyncio import tasks
import psutil
from discord.ext import commands

import discord
class Mod(commands.Cog):
    """Returns random results"""

    def __init__(self, client):
        self.client=client

    async def get_ban(self, name):
        for ban in await self.guild.bans():
            if name.isdigit():
                if ban.user.id == int(name):
                    return ban
            if str(ban.user).lower().startswith(name.lower()):
                return ban

    #Kick
    @commands.command(name="kick", aliases=["Kick", "KICK"])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def kick(self, ctx:commands.Context, member: discord.Member, *, reason=None):
        if member == ctx.author:
            await ctx.send("You can't kick yourself!" + ctx.author.mention)
        else:
            embed = discord.Embed(colour=0xFF0000)
            embed.set_author(name=f'{member} Kicked!', icon_url=member.avatar_url)
            embed.add_field(name='Kicked by ', value=f'{ctx.author.mention}', inline=False)
            embed.add_field(name='Reason', value=f'{reason}', inline=False)
            embed2 = discord.Embed(description=f'**You were kicked from {ctx.guild.name}**', colour=0xFF0000)
            embed2.add_field(name='Reason ', value=f'{reason}', inline=True)
            embed2.add_field(name='Kicked by ', value=f'{ctx.author.name}', inline=True)
            await ctx.send(embed=embed)
            await member.send(embed=embed2)
            await ctx.guild.kick(user=member,reason=reason)

    #ban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        await ctx.guild.ban(member, reason=reason)

        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=f'{member} Banned!', icon_url=member.avatar_url)
        embed.add_field(name='Banned by ', value=f'{ctx.author.mention}', inline=False)
        embed.add_field(name='Reason', value=f'{reason}', inline=False)
        embed2 = discord.Embed(description=f'**You were Banned from {ctx.guild.name}**', colour=0xFF0000)
        embed2.add_field(name='Reason ', value=f'{reason}', inline=True)
        embed2.add_field(name='Banned by ', value=f'{ctx.author.name}', inline=True)
        await ctx.send(embed=embed)
        await member.send(embed=embed2)

    #unban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member,*,reason=None):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(colour=0xFF0000)
                embed.set_author(name=f'{user} Unbanned!', icon_url=user.avatar_url)
                embed.add_field(name='Unbanned by ', value=f'{ctx.author.mention}', inline=False)
                embed.add_field(name='Reason', value=f'{reason}', inline=False)
                embed2 = discord.Embed(description=f'**You were Unbanned from {ctx.guild.name}**', colour=0xFF0000)
                embed2.add_field(name='Reason ', value=f'{reason}', inline=True)
                embed2.add_field(name='Unbanned by ', value=f'{ctx.author.name}', inline=True)
                await ctx.send(embed=embed)
                await member.send(embed=embed2)
                return

    #mute
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def mute(self, ctx, member: discord.Member,reason=None):
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(member, send_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(member, connect=False)

        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=f'{member} Muted!', icon_url=member.avatar_url)
        embed.add_field(name='Muted by ', value=f'{ctx.author.mention}', inline=False)
        embed.add_field(name='Reason', value=f'{reason}', inline=False)
        embed2 = discord.Embed(description=f'**You were Muted in {ctx.guild.name}**', colour=0xFF0000)
        embed2.add_field(name='Reason ', value=f'{reason}', inline=True)
        embed2.add_field(name='Muted by ', value=f'{ctx.author.name}', inline=True)
        await ctx.send(embed=embed)
        await member.send(embed=embed2)

    #Unmute
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unmute(self,ctx, member: discord.Member,reason=None):
        if member == ctx.author:
            return await ctx.send("You can't unmute yourself!" + ctx.author.mention)
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(member, send_messages=True)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(member, connect=True)
        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=f'{member} Unmuted!', icon_url=member.avatar_url)
        embed.add_field(name='Unmuted by ', value=f'{ctx.author.mention}', inline=False)
        embed.add_field(name='Reason', value=f'{reason}', inline=False)
        embed2 = discord.Embed(description=f'**You were unmuted in {ctx.guild.name}**', colour=0xFF0000)
        embed2.add_field(name='Reason ', value=f'{reason}', inline=True)
        embed2.add_field(name='Unmuted by ', value=f'{ctx.author.name}', inline=True)
        await ctx.send(embed=embed)
        await member.send(embed=embed2)

    #banlist
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(send_messages=True,read_messages=True,manage_guild=True)
    async def banlist(self,ctx:commands.Context):
        color = 0xc43f3f
        ban_list = await ctx.guild.bans()
        emb=discord.Embed(Title="Banlist",color=color)
        if len(ban_list)<=0:
            emb.add_field(name="Banned members",value="No one")
        else:
            for i in ban_list:
                emb.add_field(name=f"{i.user.name}#{i.user.discriminator}",value=f"Reason : {i.reason}",inline=False)
        await ctx.send(embed=emb)

    #role
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def role(self,ctx:commands.Context,mention:discord.Member,role:discord.Role):
        await mention.add_roles(role)
        await ctx.send("`Successfully given role!`")

def setup(client):
    client.add_cog(Mod(client))
