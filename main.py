import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('TOKEN')


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True           
intents.guild_messages = True  


bot = commands.Bot(command_prefix='!', intents=intents)


async def load_extensions():
 
    if not os.path.exists('./cogs'):
        print("找不到 cogs 資料夾！")
        return

    for filename in os.listdir('./cogs'):
        
        if filename.endswith('.py') and not filename.startswith('__') and "複本" not in filename:
            extension_name = f'cogs.{filename[:-3]}'
            
        
            if extension_name not in bot.extensions:
                try:
                    await bot.load_extension(extension_name)
                    print(f"✅ 成功載入擴充功能: {filename}")
                except Exception as e:
                    print(f"❌ 載入 {filename} 失敗: {e}")
            else:
                print(f"⚠️ 跳過已載入的功能: {filename}")


@bot.listen('on_message')
async def on_message_listener(message):
    if message.author.bot:
        return
    if "hi" in message.content.lower():
        await message.channel.send(f"你好 {message.author.display_name}!")

@bot.event
async def on_ready():
   
    print(f"--- 機器人已就緒 ---")
    print(f"登入身份: {bot.user}")
    print(f"ID: {bot.user.id}")
    print("------------------")


async def main():
    async with bot:
        await load_extensions() 
        await bot.start(token)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
   
        pass