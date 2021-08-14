from discord.ext import commands, tasks
from pytz import timezone
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import asyncio

def crawl_cases():
    options = webdriver.ChromeOptions()
    
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    url = 'https://corona-live.com/'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    today = soup.select('#__next > div.MainLayout__Wrapper-fslwZe.dhgRDa > div.MainLayout__Main-eibkLu.bNtKwG > div.Layout__SBox-dxfASU.gxPtSz.Layout__ChartSection-cHvvpH.byJWks > div.Layout__SBox-dxfASU.fzJGzx.Layout__SFlex-dGOlJW.Xdeos.Layout__SCol-cKWydp.iDqTgD.Chart__Wrapper-idXQdb.jGsgR > div:nth-child(2) > div > div.Layout__SBox-dxfASU.hHtHrD.Layout__SFlex-dGOlJW.Xdeos.Layout__SCol-cKWydp.iDqTgD.ChartTooltip__Wrapper-gelFCO.ZhKbp.chart-tooltip > div > div.Layout__SBox-dxfASU.gezqkt.Layout__SFlex-dGOlJW.jzrRZA.Layout__SRow-jktCWH.hwJbaK > div:nth-child(2)')[0].text[:-1]
    yesterday = soup.select('#__next > div.MainLayout__Wrapper-fslwZe.dhgRDa > div.MainLayout__Main-eibkLu.bNtKwG > div.Layout__SBox-dxfASU.gxPtSz.Layout__ChartSection-cHvvpH.byJWks > div.Layout__SBox-dxfASU.fzJGzx.Layout__SFlex-dGOlJW.Xdeos.Layout__SCol-cKWydp.iDqTgD.Chart__Wrapper-idXQdb.jGsgR > div:nth-child(2) > div > div.Layout__SBox-dxfASU.hHtHrD.Layout__SFlex-dGOlJW.Xdeos.Layout__SCol-cKWydp.iDqTgD.ChartTooltip__Wrapper-gelFCO.ZhKbp.chart-tooltip > div > div.Layout__SBox-dxfASU.gezqkt.Layout__SFlex-dGOlJW.jzrRZA.Layout__SRow-jktCWH.hwJbaK > div:nth-child(5)')[0].text[:-1]
    today, yesterday = int(today.replace(',', '')), int(yesterday.replace(',', ''))
    
    return today, yesterday

def cal_cases(n):
    diff = n[0]-n[1]
    if diff >= 0:
        return f'전일 동시간대 대비 {diff}명 증가했습니다.'
    else:
        diff *= -1
        return f'전일 동시간대 대비 {diff}명 감소했습니다.'

def now():
    return datetime.datetime.now(timezone('Asia/Seoul'))

client = commands.Bot(command_prefix='!')

@tasks.loop(seconds=1)
async def notice():
    if now().hour == 11:
        await asyncio.sleep(35999)
    if now().minute == 0 and now().second == 0:
        n = crawl_cases()
        s = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H')
        await client.get_channel(873623906907467887).send(f'{s}시 기준 확진자수는 {n[0]}명입니다.')
        await client.get_channel(873623906907467887).send(cal_cases(n))

@client.event
async def on_ready():
    notice.start()

@client.command()
async def cc(ctx): #confirmed_cases
    n = crawl_cases()
    s = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H')
    await ctx.send(f'{s}시 기준 확진자수는 {n[0]}명입니다.')
    await ctx.send(cal_cases(n))

client.run(os.environ['token'])
