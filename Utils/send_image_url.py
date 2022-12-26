import aiohttp
import io
import discord

async def send_img(message, url, filename='image.png'):
    async with aiohttp.ClientSession() as session: # creates session
            async with session.get(url) as resp: # gets image from url
                img = await resp.read() # reads image from response
                with io.BytesIO(img) as file: # converts to file-like object
                    await message.channel.send(file=discord.File(file, filename))