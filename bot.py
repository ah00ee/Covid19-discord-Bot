from discord.ext import commands
import datetime
import time
from selenium import webdriver
from bs4 import BeautifulSoup

def new_cases():
    driver = webdriver.Chrome(executable_path='C:\\Users\\nhoah\Downloads\chromedriver_win32/chromedriver.exe')
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%95%EC%A7%84%EC%9E%90+%EC%88%98'
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    t = soup.select('#_cs_production_type > div > div:nth-child(4) > div > div:nth-child(5) > div._normality > div.confirmed_status.new > div > div.tooltip_area._tooltip_wrapper > dl > div:nth-child(1) > dd.desc_em._total')[0].text
    return t


client = commands.Bot(command_prefix='!')
n = new_cases()

@client.command()
async def cc(ctx): #confirmed_cases
    s = "신규 확진자 수: "+str(n)+"명"
    await ctx.send(s)

client.run('ODczNjA3MDkwNzU5OTUwMzQ4.YQ64AQ.gzG7wpbzwhH172jrq-zpwgR3lFM')