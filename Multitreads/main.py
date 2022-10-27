import datetime
from io import BytesIO
import requests
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pika

uri = 'https://stock.adobe.com/fi/search?k=cat'


class Downloader:
    def __init__(self, link):
        if link:
            self.url = link
            self.links = []
            self.LoadPics()

    def LoadPics(self):
        self.__GetLinks()
        self.__DownloadPics()

    def __GetLinks(self):
        """получаем необходимые ссылки"""
        self.links = []
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(self.url)
            content = driver.find_elements(By.TAG_NAME, 'img')

            allowed_formats = ['png', 'jpg', 'jpeg']
            for elem in content:
                link = str(elem.get_property('src'))
                if link:
                    if link.rsplit('.', 1)[1].lower() in allowed_formats:
                        self.links.append(link)


        except:
            print('links cant be downloaded')

    def __DownloadPics(self):
        """проход по списку картинок а так же их загрузка"""
        if self.links:
            for index, link in enumerate(self.links):
                self.__Download(url=link)

    def __Download(self, url):
        """загрузка картинки по ссылке"""
        time = str(datetime.datetime.now()).replace('.', ',', ).replace(':', ',').split()
        req = requests.get(url, stream=True)
        if req.status_code == 200:
            i = Image.open(BytesIO(req.content))
            name = 'pics/img' + time[0] + time[1] + "." + url.rsplit('.', 1)[1].lower()
            i.save(name)


def Resive(ch, meth, prop, body: [bytes]):
    downloader = Downloader(body.decode("utf-8"))
    del downloader


conn_params = pika.ConnectionParameters('localhost')
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()
channel.basic_consume(queue='Messages', auto_ack=True, on_message_callback=Resive)
channel.start_consuming()
