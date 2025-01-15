# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv('bot.env')
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='Lb!', intents=intents)

links = {}


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print("Message received:", message.content)

    for k, v in links.items():
        if (message.content.startswith(f"{k}.") or
                message.content.startswith(f"https://{k}.") or
                message.content.startswith(f"http://{k}.")):
            output = str(
                f'sent by {message.author.name}\n' + message.content.replace(k, v, 1))
            print(k, v)
            await message.channel.send(output)
            await message.delete()
            break

    # Check if the message is a reply and matches the bots edited message
    if message.reference:
        if message.reference.resolved.author == bot.user and "sent by" in message.reference.resolved.content:
            original_author_name = message.reference.resolved.content.split('\n')[0][8:]

            guild = message.guild

            original_author = discord.utils.get(guild.members, name=original_author_name)
            reply_author = message.author

            if original_author:
                if reply_author.nick:
                    await message.channel.send(
                        f"{original_author.mention}, {reply_author.nick} has replied to your link")
                else:
                    await message.channel.send(
                        f"{original_author.mention}, {reply_author.name} has replied to your link")

    if message.content.strip() == f'<@!{bot.user.id}>' or message.content.strip() == f'<@{bot.user.id}>':
        await message.channel.send("Please type 'Lb!help' to get a list of commands.")

    await bot.process_commands(message)


@bot.command(
    brief="Format example: [https://old] [https://new]",
    help="Takes two args, link to be edited and replacement link. Format example: [https://old]. "
         "Omit everything after the website name. Please separate args with space."
)
async def add(ctx, arg1=None, arg2=None):
    print("add working")
    channel = ctx.channel

    if not arg1 or not arg2:
        await channel.send("Please specify a link after the command")

    elif arg1 not in links:
        links[arg1] = arg2
        await channel.send("Link added")
        print("Links after addition:", links)  # Debug print
    else:
        await channel.send("Link already added")

    print("arg1:", repr(arg1))  # Debug print
    print("arg2:", repr(arg2))  # Debug print


@bot.command(
    brief="Removes editable link. Format example: [https://youtube]",
)
async def remove(ctx, arg):
    print("remove working")
    channel = ctx.channel

    print("Argument received:", arg)
    print("Links dictionary:", links)

    if arg in links:
        del links[arg]
        await channel.send("Link removed")
        print(links)
    else:
        await channel.send("Link not found")


@bot.command(
    brief="Fetches list of links submitted in guild."
)
async def fetch(ctx):
    print("fetch working")
    channel = ctx.channel

    if links:
        for og, new in links.items():
            await channel.send(f"{og} {new}")
    else:
        await channel.send("You have no registered links")


bot.run(TOKEN)


# use nickname in the original edit instead of username
