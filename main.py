from math import sin, cos
import numpy as np
import discord, io, time, threading, asyncio, colorsys
from PIL import Image, ImageDraw
from random import randint, choice
filename = "Discord-Whooper.png"
server_id = 0
channel_id = 0
def randColor(s = -1):
    def tupleCol(h):
        return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h/360,randint(50,100)/100,randint(50,100)/100)) + (255,)
    def limit(v):
        if v < 0:
            v = 360 + v
        elif v > 359:
            v = v - 360
        return v
    ang = randint(0, 359)
    t = randint(0,9) if s == -1 else s
    if t == 0:
        h1 = ang
        h2 = ang - 120
        h3 = ang + 120
        limit(h2)
        limit(h3)
        return [tupleCol(h1),tupleCol(h2),tupleCol(h3)]
    elif t == 1:
        h1 = ang
        h2 = ang - 180
        limit(h2)
        return [tupleCol(h1),tupleCol(h2)]
    elif t == 2:
        h1 = ang
        h2 = ang - 180
        h3 = ang - 90
        h4 = ang + 90
        limit(h2)
        limit(h3)
        limit(h4)
        return [tupleCol(h1),tupleCol(h2),tupleCol(h3),tupleCol(h4)]
    elif t == 3:
        h1 = ang
        h2 = ang - 150
        h3 = ang + 150
        limit(h2)
        limit(h3)
        return [tupleCol(h1),tupleCol(h2),tupleCol(h3)]
    elif t == 4:
        h1 = randint(120, 359)
        h2 = h1 - 60
        h3 = h2 - 60
        return [tupleCol(h1),tupleCol(h2),tupleCol(h3)]
    elif t == 5:
        h1 = randint(120, 359)
        h2 = h1 - 90
        h3 = h2 - 30
        return [tupleCol(h1),tupleCol(h2),tupleCol(h3)]
    elif t == 6:
        h1 = randint(100, 309)
        h2 = h1 - 100
        h3 = h1 + 50
        return [tupleCol(h1),tupleCol(h2),tupleCol(h3)]
    elif t == 7:
        h1 = randint(50, 309)
        h2 = h1 - 50
        h3 = h1 + 50
        return [tupleCol(h1),tupleCol(h2),tupleCol(h3)]
    elif t == 8:
        h1 = randint(180, 359)
        h2 = h1 - 45
        h3 = h2 - 135
        return [tupleCol(h1),tupleCol(h2),tupleCol(h3)]
    elif t == 9:
        cols = []
        for i in range(randint(2,5)):
            cols.append(tupleCol(randint(0,359)))
        return cols
    elif t == 31:
        h1 = randint(60, 359)
        h2 = h1 - 60
        return [tupleCol(h1),tupleCol(h2)]
def generate_pix():
    CS = choice([8,12,16,20,32])
    img = Image.new('RGBA', (CS, CS), (0,0,0,0))
    color = randColor()
    for i in range(randint(0,5)):
        color += [(0,0,0,0)]
    for row in range(CS):
        for col in range(CS):
            img.putpixel((row,col), choice(color))
    new_img = Image.new('RGBA', (CS*2, CS*2), (0,0,0,0))
    new_img.paste(img,(0,0), img)
    r = img.transpose(Image.FLIP_LEFT_RIGHT)
    new_img.paste(r, (CS,0), r)
    f = new_img.transpose(Image.FLIP_TOP_BOTTOM)
    new_img.paste(f, (0,0), f)
    return new_img.resize((1000,1000), resample=Image.NEAREST)
async def send_img(mes, im):
    with io.BytesIO() as image_bin:
        fname = filename
        im.save(image_bin, "PNG", quality=100, optimize=True, progressive=True)
        image_bin.seek(0)
        mesx = await mes.send(file=discord.File(fp=image_bin, filename=fname))
client = discord.Client()
@client.event
async def on_message(message):
    if message.guild.id == server_id and not message.author.bot:
        mes = message.content.lower()
        if mes.startswith("whp gen"):
            await send_img(message.channel, generate_img())
async def rutin():
    guild = client.get_guild(server_id)
    channel = guild.get_channel(channel_id)
    while True:
        await send_img(channel, generate_pix())
        time.sleep(0.5)
@client.event
async def on_ready():
    await rutin()
print("basladi")
client.run(token)
