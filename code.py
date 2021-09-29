import os
import sys
import discord
from dotenv import load_dotenv
if True:
    sys.path.insert('Codeforces-Practice-Ladders')
    from personalised import *
    from script import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


async def get_problems(handle, min_rating, max_rating, personalised=True):
    min_rating = int(min_rating)
    max_rating = int(max_rating)
    contests = fetch_contests()
    total_problems = fetch_total_problems(contests, min_rating, max_rating)
    problems_finished = fetch_user_solves(handle)
    if personalised:
        name, link, progress, url = personalised_search(
            total_problems, problems_finished)
    else:
        name, link, progress, url = search(total_problems, problems_finished)
    return name, link, progress


async def process_msg(message):
    msg = message.split()
    print(msg)

    if len(msg) < 3 or len(msg) > 5:
        print("Usage: -gimme <handle> <min_rating> <max_rating> <generalised(optional)>")
        reply = "`Usage: -gimme <handle> <min_rating> <max_rating> <generalised(optional)>`"
        return reply, reply, reply  # error criteria
    else:
        personalised = True
        handle = msg[1]
        min_rating = msg[2]
        max_rating = msg[2]
        if len(msg) == 5:
            max_rating = msg[3]
            personalised = False
        elif len(msg) == 4:
            if msg[3] == "generalised":
                personalised = False
            elif msg[3].isdigit():
                max_rating = msg[3]
            else:
                print(
                    "Usage: -gimme <handle> <min_rating> <max_rating> <generalised(optional)>")
                reply = "`Usage: -gimme <handle> <min_rating> <max_rating> <generalised(optional)>`"
                return reply, reply, reply  # error criteria
        print("handle:", handle)
        print("min_rating:", min_rating)
        print("max_rating:", max_rating)
        print("Personalised:", personalised)

        # obj = subprocess.Popen('python3 z.py ' + handle + ' ' + min_rating + ' ' + max_rating, shell=True)
        name, link, progress = await get_problems(
            handle, min_rating, max_rating, personalised)
        return name, link, progress


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-help'):
        ret = "```-help: Get this message\n\nUsage: -gimme <handle> <rating>\nUsage: -gimme <handle> <min_rating> <max_rating>\nUsage: -gimme <handle> <min_rating> <max_rating> <generalised(optional)>\n```"
        await message.channel.send(ret)

    if message.content.startswith('-gimme'):
        name, link, progress = await process_msg(message.content)
        # await message.channel.send('I read ' + message.content)

        # Error condition
        if name == link and link == progress:
            await message.channel.send("```\nUsage: -gimme <handle> <rating>\nUsage: -gimme <handle> <min_rating> <max_rating>\nUsage: -gimme <handle> <min_rating> <max_rating> <generalised(optional)>\n```")
        else:
            ret = name+'\n'+progress+'\n'+link
            await message.channel.send(ret)

client.run(TOKEN)
