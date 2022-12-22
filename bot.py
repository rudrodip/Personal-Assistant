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
    if message.author == client.user or message.author.id != PERSONAL_ID:
        pass

    if prompt.startswith("self profile"):
        await message.channel.send(file=discord.File("babe.png"))

    if prompt.startswith("imagine"):
        prompt = message.content.lstrip("imagine:").strip()
        await message.channel.send("Generating images....")

        number_of_images = int(prompt[-1]) if prompt[-1].isdigit() else 1
        images = response_generator.image_generator(prompt, number_of_images)
        for img in images:
            await send_img(message, img)
            return

    if prompt == 'GPT OFF' and message.author.id == PERSONAL_ID and message.guild:
        GPT = False
        await message.channel.send('Turned off 🤐')
        return

    if prompt == 'GPT ON' and message.author.id == PERSONAL_ID and message.guild:
        GPT = True
        await message.channel.send('Active 😊')
        return
    
    if message.author.id == PERSONAL_ID:
        if not message.guild:
            response = response_generator.get_response(prompt)
            await message.channel.send(response)
        if message.guild and GPT:
            response = response_generator.get_response(prompt)
            await message.channel.send(response)

client.run(TOKEN)