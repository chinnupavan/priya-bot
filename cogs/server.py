
from discord.ext import commands
import sqlite3
import discord



async def open_acc(guild):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM main WHERE server_id = {guild.id}")
    result = cursor.fetchone()

    if result:
        return
    if not result:
        sql = "INSERT INTO main(server_id, w_channel,l_channel) VALUES(?,?,?)"
        val = (guild.id, 0, 0)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()






class Server(commands.Cog):
    """Returns random results"""

    def __init__(self, client):
        self.client=client


    #welcome
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    async def welcome(self,ctx:commands.Context,id=None):
        if id==None:
            await ctx.send("Please specify channel id")
            return
        else:
            await open_acc(ctx.guild)
            db = sqlite3.connect('server.db')
            cursor = db.cursor()
            sql = f"UPDATE main SET w_channel = ? WHERE server_id = ?"
            val = (id, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send("Successfully done welcome channel setup in "+"<#"+id+">")

    #leave
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    async def leave(self, ctx: commands.Context, id=None):
        if id == None:
            await ctx.send("Please specify channel id")
            return
        else:
            await open_acc(ctx.guild)
            db = sqlite3.connect('server.db')
            cursor = db.cursor()
            sql = f"UPDATE main SET l_channel = ? WHERE server_id = ?"
            val = (id, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send("Successfully done Leave channel setup in " + "<#" + id + ">")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    async def reset(self, ctx: commands.Context):
        await open_acc(ctx.guild)
        db = sqlite3.connect('server.db')
        cursor = db.cursor()
        sql = f"UPDATE main SET w_channel = ?,l_channel=? WHERE server_id = ?"
        val = (0,0, ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await ctx.send("`Successfully resetted welcome and leave setup!`")


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lockdownnone(self, ctx:commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        if ctx.guild.default_role not in channel.overwrites:
            await ctx.send(f"<#{channel.id}>  is on lockdown now")

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)

        elif (
                channel.overwrites[ctx.guild.default_role].send_messages == True
                or channel.overwrites[ctx.guild.default_role].send_messages == None
        ):
            await ctx.send(f"<#{channel.id}>  is on lockdown now")
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)

        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"lockdown removed in <#{channel.id}>")



def setup(client):
    client.add_cog(Server(client))