import os
import string
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs import hashes

PREFIX = r"f "

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
BOT_NAME = os.getenv('BOT_NAME')
INVITE_LINK = os.getenv('INVITE_LINK')
SERVER_LINK = os.getenv('SERVER_LINK')

bot_commands = [
    {
        "name": "man",
        "command": "man",
        "aliases": [
            None
        ],
        "description": "Shows the manual for the bot.",
        "syntax": f"{PREFIX}man [command]",
        "arguments": "Takes in an optional parameter for what command you want to read about."
    },
    {
        "name": "copy",
        "command": "copy",
        "aliases": [
            "cp"
        ],
        "description": f"Writes out text passed in.",
        "syntax": f"{PREFIX}copy <TEXT>",
        "arguments": "Takes in text as its only argument."
    },
    {
        "name": "binary",
        "command": "binary",
        "aliases": [
            "b",
            "bin"
        ],
        "description": "Converts text or a base 10 number into binary",
        "syntax": f"{PREFIX}binary <TEXT || NUMBER>",
        "arguments": "Takes in either text or a base 10 number as its only argument."
    },
    {
        "name": "unbinary",
        "command": "unbinary",
        "aliases": [
            "unb",
            "unbin",
        ],
        "description": f"Converts a binary number to text or string (you must specify, run {PREFIX}man unbinary for more info)",
        "syntax": f"{PREFIX}unbinary <BINARY NUMBER> [type=\"-number\"]",
        "arguments": "Takes in a binary number as its only required argument. You can also pass in a type, this defaults to -number (-n for short) to convert to a number. Pass in -text or -t in order to convert to text."
    },
    {
        "name": "hexadecimal",
        "command": "hexadecimal",
        "aliases": [
            "h",
            "hex",
        ],
        "description": f"Converts text or a base 10 number to hexadecimal",
        "syntax": f"{PREFIX}hexadecimal <TEXT || NUMBER>",
        "arguments": "Takes in a base 10 number as its only argument."
    },
    {
        "name": "unhexadecimal",
        "command": "unhexadecimal",
        "aliases": [
            "unh",
            "unhex",
        ],
        "description": f"Converts a hexadecimal number to text or string (you must specify, run {PREFIX}man hexadecimal for more info)",
        "syntax": f"{PREFIX}hexadecimal <HEXADECIMAL NUMBER>",
        "arguments": "Takes in a hexadecimal number as its only argument."
    }
]

client = commands.Bot(command_prefix=PREFIX)
client.add_cog(hashes.Hashes(client))

@client.event
async def on_ready():
    print("I'm ready to rock and roll!")
    activity = f"{PREFIX}help"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
    """guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    """
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, I'm {BOT_NAME}, and I provide a multitude of useful utilities for cybersecurity. My prefix is {PREFIX}. Type {PREFIX}help to get started."
    )


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@client.command(aliases=["cp"], help='Copies the message given')
async def copy(ctx, *args):
    res = ' '.join(args)
    if not res.strip():
        await ctx.send("That didn't work, make sure that your message contained some characters.")
        return
    await ctx.send(res)

@client.command(aliases=["bin", "b"], help='Converts a number to binary')
async def binary(ctx, *args):
    inp = ' '.join(args)
    if not inp:
        raise commands.errors.MissingRequiredArgument(inspect.Parameter(name="text_or_number", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD))
    if inp.isnumeric():
        retval = bin(int(inp)).replace("0b", "")
    else:
        res = ''.join([bin(ord(char)).replace("0b", "") for char in inp])
    await ctx.send(retval)

@client.command(aliases=["hex", "h"], help='Converts a number to hexadecimal')
async def hexadecimal(ctx, *args):
    inp = ' '.join(args)
    if not inp:
        raise commands.errors.MissingRequiredArgument(inspect.Parameter(name="text_or_number", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD))
    if inp.isnumeric():
        res = hex(int(inp)).replace("0x", "")
    else:
        res = ''.join([hex(ord(char)).replace("0x", "") for char in inp])
    await ctx.send(res)

@client.command(aliases=["unhex", "unh", "uhex", "uh"], help='Converts a hexadecimal number to decimal')
async def unhexadecimal(ctx, *args):
    inp = ''.join(args)
    if inp.isnumeric():
        res = int(inp, 16)
    else:
        res = "Sorry, text ain't supported yet."
    await ctx.send(res)

@client.command(aliases=["unbin", "unb"], help='Converts a binary number to decimal')
async def unbinary(ctx, type="-n", number: str):
    try:
        res = int(number, 2)
    except TypeError:
        await ctx.send("Sorry, that didn't work. Make sure that the number is a valid binary number.")
    await ctx.send(res)

@client.command()
async def unbintxt(ctx, *args):
    joined = ' '.join(args)
    strings = ''.join(chr(int(joined[i:i+8], 2)) for i in range(0, len(joined), 8))
    await ctx.send("In Ascii, it is " + strings)

@client.command()
async def man(ctx, command: str = None):
    global bot_commands

    if command == None:
        embed = discord.Embed(title="Help Me", description=f"**PREFIX**: `{PREFIX}`\nStuck in a pickle figuring out how to use this bot? You've come to the right place. Below are all the working commands on the bot.\nRun {PREFIX}man [command] in order to get more information about it")
        for command in bot_commands:
            embed.add_field(name=command["command"], value=command["description"])
    else:
        info = list(filter(lambda x: (x['command'] == command) or (command in x['aliases']), bot_commands))
        if (len(info) > 1):
            await ctx.send(f"Something went wrong with error code 1, please inform us in our discord server at {SERVER_LINK} and look at the error-codes channel for more information.")
            return
        elif (len(info) < 1):
            await ctx.send("The command wasn't found. Make sure you typed it in correctly.")
            return
        info = info[0]
        syntax = info['syntax']
        arguments = info['arguments']
        description = info['description']
        if (info['aliases'] == [None]):
            aliases = None
        else:
            aliases = ', '.join(info['aliases'])
        embed = discord.Embed(title=info['command'], description=f"**SYNTAX**: {syntax}\n**ALIASES**: {aliases}\n\n{arguments}\n{description}")
    await ctx.send("Hold up there, this ain't fully ready yet, here's what's done so far though", embed=embed)

@client.command(aliases=["inv"])
async def invite(ctx):
    embed = discord.Embed(name="Inviting Me", description="", color=0x008f8f)
    embed.add_field(name="Inviting me to a server", value=f"To invite me to one of your servers, use the link {INVITE_LINK}.")
    embed.add_field(name="Joining the official development server", value=f"If you just want to watch my epic attempts at making this bot, or request features, join this server: {SERVER_LINK}")

    await ctx.send(embed=embed)

@client.command(aliases=['cb'])
async def convertBase(ctx, number: int, originalBase: int = 10, base: int = 10):
    indecimal = int(str(number), originalBase)

    # The following code came from https://stackoverflow.com/a/28666223
    if indecimal == 0:
        return [0]
    digits = []
    while indecimal:
        digits.append(int(indecimal % base))
        indecimal //= base
    if not (len(list(filter(lambda x: x <= 9, digits))) < len(digits)):
        print(len(list(filter(lambda x: x <= 9, digits))) < len(digits))
        ans = ''.join(map(str, digits[::-1]))
    elif not (len(list(filter(lambda x: x <= 24, digits))) < len(digits)):
        # Convert the needed numbers to letters
        for i, x in enumerate(digits):
            if x >= 10:
                digits[i] = string.ascii_uppercase[x-10]
        ans = ''.join(map(str, digits[::-1]))
    else:
        ans = 'Digits (some could not be represented so their values are in a list):' + ', '.join(map(str, digits[::-1]))
    await ctx.send(ans)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f'The function is missing an argument. Please run {PREFIX}help for more information.')
    else:
        raise error
        #await ctx.send("something went wrong")
        #await ctx.send(f'{error}')

@client.event
async def on_message(message):
    # Make sure the message isn't from the bot
    if message.author == client.user:
        return
        
    await client.process_commands(message)

client.run(TOKEN)
