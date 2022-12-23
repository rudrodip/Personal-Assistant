import io
import discord
import os
import aiohttp
from TextProcessing import process
from TextProcessing import db

TOKEN = os.environ["BABE"]
PERSONAL_ID = 841126921886498817
PERMITTED_ACCOUNTS = db.get_accounts()

GPT, save = False, False

intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)
response_generator = process.Response('./TextProcessing/config.json')

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
    global GPT, PERMITTED_ACCOUNTS, save
    prompt = message.content.lower().strip()
    if message.author == client.user or message.author.id != PERSONAL_ID:
        pass

    if prompt.startswith("self profile"):
        await message.channel.send(file=discord.File("babe.png"))
        return

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

    if prompt == 'save off' and message.author.id == PERSONAL_ID:
        save = False
        await message.channel.send('context saving turned off 🤐')
        return

    if prompt == 'save on' and message.author.id == PERSONAL_ID:
        save = True
        await message.channel.send('context saving turned on 😊')
        return

    if prompt == 'refresh' and message.author.id == PERSONAL_ID:
        PERMITTED_ACCOUNTS = db.get_accounts()
        await message.channel.send('refreshed all permitted accounts 😊')
        return
    
    if message.author.id == PERSONAL_ID:
        if not message.guild:
            response = response_generator.get_response(prompt)
            await message.channel.send(response)
        if message.guild:
            if prompt.startswith('babe'):
                prompt = prompt.lstrip("babe").strip() 
                response = response_generator.get_response(prompt, save)
                await message.channel.send(response)

    if str(message.author.id) in PERMITTED_ACCOUNTS and prompt.startswith('sergio'):
        prompt = prompt.lstrip("sergio").strip()
        response = response_generator.get_response(prompt, author=PERMITTED_ACCOUNTS[str(message.author.id)], save=save)
        response = f'<@{message.author.id}> {response}'
        await message.channel.send(response)

client.run(TOKEN)