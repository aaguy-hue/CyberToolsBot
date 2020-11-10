import discord
from discord.ext import commands
import hashlib
import io
import requests
import inspect

class Hashes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def hashing(self, kind: str, text: str):
        if kind == "sha256":
            the_hash = hashlib.sha256()
        elif kind == "sha512":
            the_hash = hashlib.sha512()
        elif kind == "md5":
            the_hash = hashlib.md5()
        elif kind == "sha1":
            the_hash = hashlib.sha1()
        # Read the bytes in small blocks so it can handle large files
        for byte_block in iter(lambda: text.read(4096),b""):
            the_hash.update(byte_block)
        return the_hash.hexdigest()

    @commands.command()
    async def sha256(self, ctx, *args):
        joined = ' '.join(args)
        if not joined.strip():
            if (files := ctx.message.attachments):
                for i, f in enumerate(files):
                    text = io.BytesIO(io.StringIO(requests.get(f.url).text).read().encode('utf8'))
            else:
                raise commands.errors.MissingRequiredArgument(inspect.Parameter(name="text_or_file", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD))
        else:
            text = io.BytesIO(io.StringIO(joined).read().encode('utf8'))
        await ctx.send(self.hashing("sha256", text))

    @commands.command()
    async def sha512(self, ctx, *args):
        joined = ' '.join(args)
        if not joined.strip():
            if (files := ctx.message.attachments):
                for i, f in enumerate(files):
                    text = io.BytesIO(io.StringIO(requests.get(f.url).text).read().encode('utf8'))
            else:
                raise commands.errors.MissingRequiredArgument(inspect.Parameter(name="text_or_file", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD))
        else:
            text = io.BytesIO(io.StringIO(joined).read().encode('utf8'))
        await ctx.send(self.hashing("sha512", text))

    @commands.command()
    async def md5(self, ctx, *args):
        joined = ' '.join(args)
        if not joined.strip():
            if (files := ctx.message.attachments):
                for i, f in enumerate(files):
                    text = io.BytesIO(io.StringIO(requests.get(f.url).text).read().encode('utf8'))
            else:
                raise commands.errors.MissingRequiredArgument(inspect.Parameter(name="text_or_file", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD))
        else:
            text = io.BytesIO(io.StringIO(joined).read().encode('utf8'))
        await ctx.send(self.hashing("md5", text))

    @commands.command()
    async def sha1(self, ctx, *args):
        joined = ' '.join(args)
        if not joined.strip():
            if (files := ctx.message.attachments):
                for i, f in enumerate(files):
                    text = io.BytesIO(io.StringIO(requests.get(f.url).text).read().encode('utf8'))
            else:
                raise commands.errors.MissingRequiredArgument(inspect.Parameter(name="text_or_file", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD))
        else:
            text = io.BytesIO(io.StringIO(joined).read().encode('utf8'))
        await ctx.send(self.hashing("sha1", text))
