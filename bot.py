from discord.ext import commands, tasks
import datetime
import time
from selenium import webdriver
from bs4 import BeautifulSoup

def crawl_cases():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path='C:\\Users\\nhoah\Downloads\chromedriver_win32/chromedriver.exe', options=options)

    url = 'https://corona-live.com/'
    driver.get(url)
    time.sleep(1)
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

client = commands.Bot(command_prefix='!')
n = crawl_cases()

@tasks.loop(seconds=1)
async def notice():
    if datetime.datetime.now().minute == 0 and datetime.datetime.now().second == 0:
        s = datetime.datetime.now().strftime('%Y-%m-%d %H')
        await client.get_channel('(int)Your channel ID').send(f'{s}시 기준 확진자수는 {n[0]}명입니다.')
        await client.get_channel('(int)Your channel ID').send(cal_cases(n))

@client.event
async def on_ready():
    notice.start()

@client.command()
async def cc(ctx): #confirmed_cases
    s = datetime.datetime.now().strftime('%Y-%m-%d %H')
    await ctx.send(f'{s}시 기준 확진자수는 {n[0]}명입니다.')
    await ctx.send(cal_cases(n))

client.run('Your Token')