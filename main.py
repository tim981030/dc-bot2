import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# 1. 環境設定
load_dotenv()
token = os.getenv('TOKEN')

# 2. Flask 虛擬伺服器 (讓 Render 偵測到 Port)
app = Flask('')

@app.route('/')
def home():
    return "機器人正在運行中！"

def run_flask():
    # Render 會自動分配 PORT，若沒有則預設 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True # 確保主程式結束時執行緒也會關閉
    t.start()

# 3. Bot 設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True           
intents.guild_messages = True  

bot = commands.Bot(command_prefix='!', intents=intents)

# 4. 載入 Cogs 邏輯
async def load_extensions():
    if not os.path.exists('./cogs'):
        print("找不到 cogs 資料夾！")
        return

    for filename in os.listdir('./cogs'):
        # 過濾：只讀取 .py，排除底線開頭檔案，排除複本
        if filename.endswith('.py') and not filename.startswith('__') and "複本" not in filename:
            extension_name = f'cogs.{filename[:-3]}'
            
            if extension_name not in bot.extensions:
                try:
                    await bot.load_extension(extension_name)
                    print(f"✅ 成功載入擴充功能: {filename}")
                except Exception as e:
                    print(f"❌ 載入 {filename} 失敗: {e}")

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

# 5. 主程式入口
async def main():
    # 在啟動 Bot 之前，先啟動 Flask
    print("正在啟動 Web 伺服器...")
    keep_alive()
    
    async with bot:
        await load_extensions()
        await bot.start(token)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("機器人已關閉")
