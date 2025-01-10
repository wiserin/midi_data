import requests
from bs4 import BeautifulSoup
import cloudscraper
from lxml import etree 
import app.database.requests as db

scraper = cloudscraper.create_scraper()


class ParseLinks:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()


    def get_html(self, url: str) -> str:
        response = self.scraper.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Ошибка загрузки:", response.status_code)


    def get_links(self, html: str) -> None:
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all('article', attrs={'class': 'relative'})
        l = []
        for link in links:
            l.append(link.find_all('a')[0].get('href'))

        db.add_links(l)
    

    def parse(self, count) -> None:
        for i in range(1, count + 1):
            html = self.get_html(f'https://bitmidi.com/?page={i}')
            self.get_links(html)