import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# --- Discord Token ---
# 載入 .env 檔案中的環境變數
load_dotenv()
# 從環境變數中取得 Discord Bot Token (Render 環境變數名稱要一致)
token = os.getenv("token")

if token is None:
    # 如果找不到 token，拋出錯誤提醒使用者設定
    raise ValueError("Discord token not found! Please set 'token' in environment variables.")

# --- Discord Bot Setup ---
# 設定 Intenets 權限，確保可以讀取訊息內容和公會訊息
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True

# 創建 Bot 實例，設定指令前綴為 "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 遊戲邏輯變數 (全局狀態) ---
n = 1  # 遊戲中目前需要的數字
last_user_id = None  # 上一個發送正確數字的使用者 ID
# 請將此 ID 替換為您實際要進行遊戲的頻道 ID
channel_id = 1446455483689992305

@bot.event
async def on_message(message):
    await message.channal.send(f"ok")


# --- Flask Web Service for Render 保活 (Keep-Alive) ---
app = Flask("")

@app.route("/")
def home():
    # Render 會定期訪問此路由來保持 Bot 服務運行
    return "Bot is running!"

def run_flask():
    # 取得環境變數中的 PORT，預設為 5000
    port = int(os.environ.get("PORT", 5000))
    print(f"Flask running on port {port}")
    # 啟動 Flask 伺服器
    app.run(host="0.0.0.0", port=port)

# 在一個單獨的執行緒中啟動 Flask 服務，避免阻塞 Bot 的主線程
flask_thread = Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()


# --- Run Discord Bot ---
print("Starting Discord bot...")
bot.run(token)
