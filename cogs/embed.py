import discord
from discord.ext import commands

class EmbedCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sendembed(self, ctx):
        msg = discord.Embed(
            title="標題",
            description="說明",
            color=discord.Color.red()
        )
        msg.add_field(name="名字1", value="數值1", inline=True)
        msg.add_field(name="名字2", value="數值2", inline=True)
        
        if ctx.author.avatar:
            msg.set_image(url=ctx.author.avatar.url)
        
        msg.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        msg.set_footer(text="文字", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        await ctx.send(embed=msg)  # ✅ 只呼叫一次

    @commands.command()
    async def embed_with_emoji(self, ctx):
        emoji = "<:MyCustomEmoji:123456789012345678>"
        msg = discord.Embed(
            title=f"表符 {emoji}",
            description="這是表符",
            color=discord.Color.blue()
        )
        await ctx.send(embed=msg)

async def setup(bot):
    await bot.add_cog(EmbedCommands(bot))
