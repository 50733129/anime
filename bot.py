import discord
from discord.ext import commands
import json
import requests
from bs4 import BeautifulSoup

# 啟用所有 intents
intents = discord.Intents.all()

# 讀取設定檔 load settings
with open('./PyBot-backBone-master/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# 創建 Bot 實例
bot = commands.Bot(command_prefix='$', intents=intents)

# Bot完成啟動後事件
@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_command_error(ctx, error):
    # 處理指令錯誤
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("指令輸入錯誤，請嘗試其他指令。")

@bot.command()
async def ping(ctx):
    #Bot 延遲
    await ctx.send(f'{round(bot.latency*1000)} ms')



# 定義 HTTP 請求的 headers，模擬瀏覽器行為
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
}

@bot.command()
async def s(ctx, name):
    # 發送 HTTP GET 請求，獲取動漫搜尋結果頁面
    r = requests.get(f'https://ani.gamer.com.tw/search.php?keyword={name}', headers=headers)

    if r.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML 內容
        soup = BeautifulSoup(r.text, 'html.parser')

        # 選擇特定的元素進行解析
        newanime_item = soup.select_one('.theme-list-block')
        newanime_itemss = soup.select_one('.animate-theme-list')
        anime_items = newanime_item.select('.theme-list-main')
        s = len(anime_items)

        if int(s) > 0:  # 如果有動畫結果
            for anime_item in anime_items:
                # 抓取動畫名稱
                anime_name = anime_item.select_one('.theme-info-block > p').text.strip()
                await ctx.send(anime_name)

                # 抓取動畫觀看網址
                anime_href = newanime_itemss.select_one("a", {"class": "theme-list-main"}).attrs['href']
                await ctx.send(f'https://ani.gamer.com.tw/{anime_href}')

        else:  # 如果沒有動畫結果
            await ctx.send('抱歉這裡沒有您想看的動漫')



# 執行 Bot
if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
	
