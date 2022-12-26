import discord
import os
from TextProcessing import process
from Utils import send_image_url

TOKEN = os.environ["BABE"]
PERSONAL_ID = 841126921886498817

intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)
response_generator = process.Response()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    prompt = message.content.lower().strip()

    if message.author == client.user or message.author.id != PERSONAL_ID:
        pass

    if prompt.startswith("self profile"):
        await message.channel.send(file=discord.File("babe.png"))
        return

    if prompt.startswith("!"):
        prompt = prompt.lstrip('!').strip()
        response = await response_generator.get_response(prompt)
        await message.channel.send(response)
        return

client.run(TOKEN)