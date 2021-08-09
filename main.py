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
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
from io import BytesIO
from discord.ext import commands,tasks
import phonenumbers
from phonenumbers import geocoder,carrier


#from imgurpython import ImgurClient
from config import *


intents = discord.Intents.default()
intents.members = True

client=commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX),intents=intents)
client.remove_command("help")


#imgur
#a=imgur_a
#b=imgur_b
#cc=ImgurClient(a,b)


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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"p!help | {len(client.guilds)} servers"),status=discord.Status.idle)
    await asyncio.sleep(30)
    c=0
    for g in client.guilds:
        for i in g.members:
            c=c+1
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name=f"p!help | {c} Users"),status=discord.Status.idle)




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
async def on_member_join(member):
    op = Image.open("bg.jpg")
    b = op.filter(ImageFilter.GaussianBlur(5))

    b = ImageOps.expand(b, 4, 0xf7f1e3)

    av = member.avatar_url_as(size=128)
    data = BytesIO(await av.read())
    pfp = Image.open(data)
    pfp = pfp.resize((160, 160))
    pfp = ImageOps.expand(pfp, 4, 0xf7f1e3)
    b.paste(pfp, (280, 160))
    b.save("b2.png")

    img = Image.open("b2.png")
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype("fonts/my.ttf", 40)
    font2 = ImageFont.truetype("fonts/name.ttf", 60)
    string = member.name + "#" + member.discriminator
    draw.text((230, 70), "WELCOME", "white", font=font1)
    draw.text((220, 360), string, "white", font=font2)

    img.save("b3.png")
    try:

        embed = discord.Embed(title="Welcome to " + member.guild.name, description=member.mention+" is our "+str(len(member.guild.members))+"th member.")
        file = discord.File("b3.png")
        embed.set_image(url="attachment://b3.png")
        db = sqlite3.connect('server.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE server_id = {member.guild.id}")
        result = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        await member.send(embed=embed)
        embed.set_thumbnail(url=member.guild.icon_url)
        embed.set_footer(text="Totale members : " + str(len(member.guild.members)))
        channel = client.get_channel(result[1])
        await channel.send(file=file, embed=embed)
    except:
        return



@client.event
async def on_member_remove(member):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM main WHERE server_id = {member.guild.id}")
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    try:
        embed = discord.Embed(title=member.guild.name)
        embed.add_field(name="see you again!", value=member.name)
        await member.send(embed=embed)

        em = discord.Embed(
        title="Bye bye " + member.name + "!",
        description="see you again in " + member.guild.name,
        color=discord.Color.green()
        )
        em.set_thumbnail(url=member.avatar_url)
        em.set_footer(text="Total members : " + str(len(member.guild.members)))
        channel = client.get_channel(result[2])
        await channel.send(embed=em)
    except:
        return



@client.event
async def on_message(message):
    if "p!phn" in message.content.lower():
        s=message.content.lower()
        phone_number = phonenumbers.parse(s[5:])
        embed = discord.Embed(title="Your number details",
                              description="Region : " + geocoder.description_for_number(phone_number, 'en') + "\n" +
                                          "Carier : " + carrier.name_for_number(phone_number, 'en')

                              )
        await message.author.send(embed=embed)
    if not message.author.bot:
        print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

        if client.user.mentioned_in(message):
            await message.channel.send("You can type `p!help` for more info")

        if 'p!nsfw' in message.content.lower():
            if message.channel.is_nsfw():
                #it = cc.get_album_images('HtpJJL4')
                #m = random.choice(it)
                #em = discord.Embed()
                #em.set_image(url=m.link)
                #await message.channel.send(embed=em)
                await message.channel.send("Comming soon!")
            else:
                await message.channel.send("Please use this command in NSFW channel"+message.author.mention)


    # to stop message event
    await client.process_commands(message)


#-----------------commands errors ---------------------#

#invalid commands
@client.event
async def on_command_error(ctx,error):
    #bot permissions error
    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        m = 'I do not have **{}** permission(s)!'.format(fmt)
        await ctx.send(m)
        return
    #user permission error
    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You do not have **{}** permission(s)!'.format(fmt)
        await ctx.send(_message)
        return
    #cooldown errors
    if isinstance(error,commands.CommandOnCooldown):
        secs=error.retry_after
        mes = f"{secs // 3600:02.0f}:{(secs // 60) % 60:02.0f}:{secs % 60:02.0f}"
        if "tada" in ctx.message.content:
            await ctx.send("wait for : " + mes )
        elif "spin" in ctx.message.content:
            await ctx.send("please try again in : "+mes)
        elif "mining" or "mine" in ctx.message.content:
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


#-----------------------simple commands-------------------------#

@client.command()
async def blur(ctx):

    op = Image.open("bg.jpg")
    b = op.filter(ImageFilter.GaussianBlur(8))

    b = ImageOps.expand(b, 4, 0xf7f1e3)

    av=ctx.author.avatar_url_as(size=128)
    data = BytesIO(await av.read())
    pfp=Image.open(data)
    pfp=pfp.resize((160,160))
    pfp=ImageOps.expand(pfp, 4, 0xf7f1e3)
    b.paste(pfp,(280,160))
    b.save("b2.png")

    img=Image.open("b2.png")
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype("fonts/my.ttf",40)
    font2 = ImageFont.truetype("fonts/name.ttf",60)
    string=ctx.author.name+"#"+ctx.author.discriminator
    draw.text((230,70),"WELCOME","white",font=font1)
    draw.text((220,360),string,"white",font=font2)

    img.save("b3.png")

    embed=discord.Embed(title="Welcome to "+ctx.guild.name,description=ctx.author.mention)
    file=discord.File("b3.png")
    embed.set_image(url="attachment://b3.png")
    await ctx.send(file=file,embed=embed)

@client.command()
async def btc(ctx,cur=None):
    if cur==None:
        cur='USD'
    cur=cur.upper()
    url1="https://api.coindesk.com/v1/bpi/currentprice/"
    url2=cur+".json"
    url = url1+url2
    try:
        async with aiohttp.ClientSession() as session:  # Async HTTP request
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            #await ctx.channel.send("Bitcoin price is: INR " + response['bpi']['INR']['rate'])
            st=response['bpi'][cur]['rate']+ f" {cur}"
            embedd = discord.Embed(description="<a:btcinr:860587207398916096>"+" Bitcoin price : `{0}`".format(st), colour=0x0DDCFF)
            await ctx.channel.send(embed=embedd)
    except:
        await ctx.channel.send("`Invalid currency code!\ncheck currency codes\n`"+"https://pastebin.com/pGeEtYHR")

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

@client.command()
async def info(ctx):
    my_system = platform.uname()
    embed = discord.Embed(colour=0xc8dc6c)
    embed.add_field(name="Architecture : ", value=platform.architecture()[0])
    embed.add_field(name="Machine : ", value=platform.machine())
    embed.add_field(name="Node : ", value=platform.node())
    embed.add_field(name="System : ", value=platform.system())
    embed.add_field(name="Processor : ", value=my_system.processor)
    await ctx.send(embed=embed)

client.run(TOKEN,reconnect=True)

