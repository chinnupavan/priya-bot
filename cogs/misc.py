import asyncio
import os
from asyncio import tasks
import psutil
from discord.ext import commands

import discord


class Misc(commands.Cog):
    """Returns random results"""
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx: commands.Context):
        pembedVar = discord.Embed(
            description="<a:ping9100:859882795651825695>" + " Latency  " +
            f"```{round(self.client.latency * 1000)} ms```",
            color=0xFF5733)
        await ctx.send(embed=pembedVar)

    # timer
    @commands.command()
    async def timer(self, ctx: commands.Context, seconds):
        try:
            secondint = int(seconds)
            if secondint < 1 or secondint > 300:
                embedVar = discord.Embed(
                    description="<a:timer9100:859871243054481438>" + " : " +
                    " please use range between 1-300s",
                    color=0xFF5733)
                await ctx.send(embed=embedVar)
            else:

                embedVar = discord.Embed(
                    description="<a:timer9100:859871243054481438>" +
                    " Remaining : " + f"{seconds}",
                    color=0xFF5733)

                message = await ctx.send(embed=embedVar)
                await asyncio.sleep(1)
                for i in range(secondint - 1, -1, -1):
                    embedVar = discord.Embed(
                        description="<a:timer9100:859871243054481438>" +
                        " Remaining : " + f"{i}",
                        color=0xFF5733)
                    await message.edit(embed=embedVar)
                    await asyncio.sleep(1)
                await message.delete()
                embedVar = discord.Embed(
                    description="<a:timer9100:859871243054481438>" + " : " +
                    ctx.author.mention + " Your countdown " + f"{seconds}s " +
                    "Has ended!",
                    color=0xFF5733)
                await ctx.send(embed=embedVar)

        except ValueError:
            embedVar = discord.Embed(
                description="<a:timer9100:859871243054481438>" +
                " Must be a number!",
                color=0xFF5733)
            await ctx.send(embed=embedVar)


def setup(client):
    client.add_cog(Misc(client))
