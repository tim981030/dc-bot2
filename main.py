import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv

# 讀取 .env
load_dotenv()
token = os.getenv('TOKEN')

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True

# 建立 bot
bot = commands.Bot(command_prefix='!', intents=intents)

# 載入 cogs
async def load_extensions():
    # ... (此處保持不變)
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# ✅ 新增：使用 @bot.listen() 處理非指令訊息
# 這樣不會干擾 Bot 內建的指令處理器 (process_commands)
@bot.listen('on_message')
async def on_message_listener(message):
    if message.author.bot:
        return

    if "hi" in message.content.lower():
        await message.channel.send(f"你好 {message.author.display_name}!")
        
# ❌ 移除舊的 on_message 函式 (已不需手動呼叫 process_commands)
# @bot.event
# async def on_message(message):
#     ... (原有的程式碼已移除)

@bot.event
async def on_ready():
    print(f"{bot.user} logged in!")

# 正常 main()
async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())