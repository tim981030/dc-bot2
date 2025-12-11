from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # 確保指令能被正常處理（如果你有指令）
        await self.bot.process_commands(message)

        # 每當有人說話就回覆 1
        await message.channel.send("1")

# setup 函數必須在 class 外面
async def setup(bot):
    await bot.add_cog(OnMessage(bot))
