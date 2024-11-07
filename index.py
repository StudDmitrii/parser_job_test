import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

#params 
quote_limit = 10

#const
START_URL = 'https://quotes.toscrape.com'
NEXT_BTN_SELECTOR = '.next > a'

#init
driver = webdriver.Chrome()
driver.get(START_URL)
data = []

#functions
def next_page():
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, NEXT_BTN_SELECTOR)
        next_btn.click()
    except Exception:
        return False

def export(data):
    with open('./data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

#main
quote_left = quote_limit
while quote_left > 0:
    document = BeautifulSoup(driver.page_source)
    quotes = document.select('div.col-md-8 > div')
    for quote in quotes:
        text = quote.select('.text')[0].text
        author_name = quote.select('.author')[0].text
        author_link = START_URL + quote.select('.author ~ a')[0].get('href')
        tags = [{'tag':tag.text, 'link':START_URL + tag.get('href')} for tag in quote.select('.tags > .tag')]
        data.append({
            'text':text,
            'author':{
                'name':author_name,
                'link':author_link
            },
            'tags':tags
        })
        quote_left -= 1
        if quote_left == 0: break
    if next_page() == False: break

export(data)
driver.close()