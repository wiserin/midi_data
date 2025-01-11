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
        """
        Получение html страницы

        :param url: ссылка на требуемую страницу
        """

        response = self.scraper.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Ошибка загрузки:", response.status_code)


    def get_links(self, html: str) -> None:
        """
        Получение ссылок на страницы файлов из html

        :param html: html документ из которого требуется извлечь ссылки
        """

        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all('article', attrs={'class': 'relative'})
        l = []
        for link in links:
            l.append(link.find_all('a')[0].get('href'))

        db.add_links(l)


    def parse(self, count) -> None:
        """
        Парсит ссылки на страницы файлов и сохраняет их в БД

        :param count: Целевое количество страниц для парсинга
        """

        for i in range(1, count + 1):
            html = self.get_html(f'https://bitmidi.com/?page={i}')
            self.get_links(html)
            if i % 50 == 0:
                print(f'Скопировано: {i} страниц')



class ParseMidi(ParseLinks):
    def __init__(self):
        super().__init__()

    def get_file_link(self, html) -> str:
        """
        Получение ссылки на файл из html

        :param html: html документ из которого требуется извлечь ссылки
        """

        soup = BeautifulSoup(html, 'html.parser')
        link = soup.find_all('div', attrs={'class': 'w-50-ns'})[1]
        link = link.find_all('a')[0].get('href')
        return link


    def parse_midi(self, count) -> None:
        """
        Парсит ссылки на файлы и скачивает их

        :param count: Целевое количество скачаных файлов
        """

        for midi in range(1, count + 1):
            link = db.get_link(midi)
            url = f'https://bitmidi.com{link}'
            html = self.get_html(url)
            link = self.get_file_link(html)
            response = requests.get(f'https://bitmidi.com{link}', stream=True)

            with open(f'data{link}', "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            if midi % 25 == 0:
                print(f'Скачано: {midi}')