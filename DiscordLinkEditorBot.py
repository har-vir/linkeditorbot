# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv('bot.env')
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

original_author = None

@client.event
async def on_message(message):

    global original_author
    original_author = message.author

    if message.author == client.user:
        return

    if message.content.startswith('https://twitter'):
        output = str(
            f'sent by {original_author.name}\n' + message.content.replace('https://twitter', 'https://vxtwitter'))
        await message.channel.send(output)
        await message.delete()
    elif message.content.startswith('https://x'):
        output = str(
            f'sent by {original_author.name}\n' + message.content.replace('https://x', 'https://vxtwitter'))
        await message.channel.send(output)
        await message.delete()

    # Check if the message is a reply and matches the bot's edited message
    if message.reference:
        referenced_message = await message.channel.fetch_message(message.reference.message_id)
        if referenced_message.author == client.user and referenced_message.content.startswith(f'sent by {original_author.name}'):
            await message.channel.send(original_author.mention)

client.run(TOKEN)



# basic functionality done, can replace x and twitter with vxtwitter
# now just make sure it's case insensitive
# then also delete users post
# and add which user sent message in bot's message
#DELETE PINGED MSG ONCE OP REPLIES TO QUOTED MSG
#message.author.mention to ping op
#what happens if someone else uses the bot, will the original_author variable be overwritten? and so it will now reference the latest user of the bot no matter which message you ping