# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv('bot.env')
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = discord.Client(intents = intents)

members_by_name = {}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('https://twitter'):
        output = str(
            f'sent by {message.author.name}\n' + message.content.replace('https://twitter', 'https://vxtwitter'))
        await message.channel.send(output)
        await message.delete()
    elif message.content.startswith('https://x'):
        output = str(
            f'sent by {message.author.name}\n' + message.content.replace('https://x', 'https://vxtwitter'))
        await message.channel.send(output)
        await message.delete()

    # Check if the message is a reply and matches the bot's edited message
    if message.reference:
        if message.reference.resolved.author == client.user:
            original_author_name = message.reference.resolved.content.split('\n')[0][8:]

            guild = message.guild

            await guild.fetch_members(limit=None).flatten()
            original_author = discord.utils.get(guild.members, name = original_author_name)
            reply_author = message.author

            if original_author:
                if reply_author.nick:
                    await message.channel.send(f"{original_author.mention}, {reply_author.nick} has replied to your link")
                else:
                    await message.channel.send(f"{original_author.mention}, {reply_author.name} has replied to your link")

client.run(TOKEN)



# basic functionality done, can replace x and twitter with vxtwitter
# now just make sure it's case insensitive
# then also delete users post
# and add which user sent message in bot's message
#DELETE PINGED MSG ONCE OP REPLIES TO QUOTED MSG
#message.author.mention to ping op
#use nickname in the original edit instead of username