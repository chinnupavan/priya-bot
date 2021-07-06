import asyncio
import os
from asyncio import tasks

import youtube_dl
from discord.ext import commands


class Music(commands.Cog):
    """Returns random results"""

    def __init__(self, client):
        self.client=client

    @commands.command()
    async def music(self,ctx:commands.Context):
        await ctx.send("comming soon")



def setup(client):
    client.add_cog(Music(client))