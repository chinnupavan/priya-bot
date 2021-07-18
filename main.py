import asyncio
import datetime
import json
import os
import platform
import random
import sqlite3
from datetime import timedelta
import datetime, time
import aiohttp
import discord


from discord.ext import commands,tasks
from imgurpython import ImgurClient
from config import *

client=commands.Bot(command_prefix=PREFIX)
client.remove_command("help")

#imgur
a=imgur_a
b=imgur_b
cc=ImgurClient(a,b)


async def open_acc(user):
    db = sqlite3.connect('bank.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if result:
        return
    if not result:
        sql = "INSERT INTO main(member_id, wallet, bank,gold,diamonds,silver,staff,machine) VALUES(?,?,?,?,?,?,?,?)"
        val = (user.id, 500, 0,0,0,0,0,0)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@tasks.loop(minutes=1)
async def change_pr():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"p!help | {len(client.guilds)} servers"))
    await asyncio.sleep(30)
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name=f"p!help | {len(client.users)} users"))


#bot login
@client.event
async def on_ready():

    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="p!help"))
    print(f"We have logged in as {client.user}")
    print(f"ID {client.user.id}")
    global s
    s = time.time()

    # load all cogs
    for folder in os.listdir("./cogs"):
        if folder.endswith(".py"):
            try:
                client.load_extension(f"cogs.{folder[:-3]}")
                print((f"loaded {folder}"))
            except Exception as e:
                print(f"{e}")
    await change_pr.start()

#-------------------------------message events---------------------------#
@client.event
async def on_message(message):
    if not message.author.bot:
        print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
        if message.content.lower() == "p!id":
            em = discord.Embed(description=message.author, color=0x79FF08)
            await message.channel.send(embed=em)

        if "p!avatar" in message.content.lower():
            embedd = discord.Embed(title=message.author.name, colour=0x0DDCFF)
            embedd.set_image(
                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=128".format(message.author))
            await message.channel.send(embed=embedd)

        if 'p!nsfw' in message.content.lower():
            if message.channel.is_nsfw():
                it = cc.get_album_images('HtpJJL4')
                m = random.choice(it)
                em = discord.Embed()
                em.set_image(url=m.link)
                await message.channel.send(embed=em)
            else:
                await message.channel.send("Please use this command in NSFW channel"+message.author.mention)


    # to stop message event
    await client.process_commands(message)


#-----------------commands errors ---------------------#

#invalid commands
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        secs=error.retry_after
        mes = f"{secs // 3600:02.0f}:{(secs // 60) % 60:02.0f}:{secs % 60:02.0f}"
        if "tada" in ctx.message.content:
            await ctx.send("wait for : " + mes )
        elif "spin" in ctx.message.content:
            await ctx.send("please try again in : "+mes)
        elif "mining" in ctx.message.content:
            await open_acc(ctx.author)
            member = ctx.author

            db = sqlite3.connect('bank.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM main WHERE member_id = {member.id}")
            result = cursor.fetchone()
            db.commit()
            cursor.close()

            val = result[6]
            if val>=1:
                secs = error.retry_after-(21600//2)
                mes = f"{secs // 3600:02.0f}:{(secs // 60) % 60:02.0f}:{secs % 60:02.0f}"
                await ctx.send("Mining will end in : " + mes)
            else:
                secs = error.retry_after
                mes = f"{secs // 3600:02.0f}:{(secs // 60) % 60:02.0f}:{secs % 60:02.0f}"
                await ctx.send("Mining will end in : " + mes)


    #await ctx.send("timee")
#-----------------------simple commands-------------------------#
@client.command()
async def btc(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/INR.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        #await ctx.channel.send("Bitcoin price is: INR " + response['bpi']['INR']['rate'])
        st=response['bpi']['INR']['rate']+" INR"
        embedd = discord.Embed(description="<a:btcinr:860587207398916096>"+" Bitcoin price : `{0}`".format(st), colour=0x0DDCFF)
        await ctx.channel.send(embed=embedd)

@client.command()
async def clear(ctx,args):
    s =int(args)
    dele = await ctx.channel.purge(limit=s)
    emd = discord.Embed(description=f"{len(dele):,} messages have been deleted.")
    await ctx.channel.send(embed=emd, delete_after=3)

@client.command()
async def uptime(ctx):
    ss=platform.system()
    current_time = time.time()
    difference = int(round(current_time - s))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(colour=0xc8dc6c)
    embed.add_field(name="Uptime", value=text)
    #embed.add_field(name="Platform", value=ss,inline=False)
    try:
        await ctx.send(embed=embed)
    except discord.HTTPException:
        await ctx.send("Current uptime: " + text)

#get user id
@client.command()
async def userid(ctx,member:discord.Member):
    await ctx.send(member.id)


client.run(TOKEN,reconnect=True)

