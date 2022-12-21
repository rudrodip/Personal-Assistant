import io
import discord
import os
import aiohttp
from TextProcessing import process

TOKEN = os.environ["BABE"]
PERSONAL_ID = 841126921886498817

GPT = False

intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)
response_generator = process.Response('./TextProcessing/Database/config.json')

async def send_img(message, url):
    async with aiohttp.ClientSession() as session: # creates session
            async with session.get(url) as resp: # gets image from url
                img = await resp.read() # reads image from response
                with io.BytesIO(img) as file: # converts to file-like object
                    await message.channel.send(file=discord.File(file, "imagination.png"))

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global GPT
    prompt = message.content
    if message.author == client.user and message.author.id != PERSONAL_ID:
        pass

    if prompt.startswith("self profile"):
        await message.channel.send(file=discord.File("babe.png"))

    if prompt.startswith("imagine"):
        prompt = message.content.lstrip("imagine:").strip()
        await message.channel.send("Generating images....")
        images = response_generator.image_generator(prompt)
        for img in images:
            await send_img(message, img)

        await message.channel.send(prompt)

    if prompt == 'GPT OFF' and message.author == client.user:
        GPT = False
        await message.channel.send('Turned off 🤐')

    if prompt == 'GPT ON' and message.author == client.user:
        GPT = True
        await message.channel.send('Active 😊')
    
    if message.author.id == PERSONAL_ID and GPT:
        if not prompt.startswtih("GPT"):
            response = response_generator.get_response(prompt)
            if response:
                await message.channel.send(response)

client.run(TOKEN)