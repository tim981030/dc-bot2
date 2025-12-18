import discord
from discord.ext import commands

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def delete_msg(self, ctx, amount: int):
        # 確保這行只會印出一次
        print(f">>> 【測試 A】收到指令：{ctx.author}")
        
        try:
            # 加上 1 是為了刪除使用者輸入的那則 !clear 指令
            deleted = await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"✅ 已成功刪除 {len(deleted)-1} 則訊息！", delete_after=5)
            print(f">>> 執行完畢，成功刪除 {len(deleted)-1} 則。")
        except discord.Forbidden:
            print("❌ 錯誤：機器人缺少『管理訊息』或『讀取歷史訊息』權限。")
            await ctx.send("我沒有權限執行此操作，請檢查我的權限設定。")
        except Exception as e:
            print(f"❌ 發生未知錯誤: {e}")
            await ctx.send(f"執行失敗，原因：{e}")

async def setup(bot):
    await bot.add_cog(moderation(bot))