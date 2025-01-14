import requests
import fake_useragent
import multiprocessing
from bs4 import BeautifulSoup

class ParseProxy():
    user = fake_useragent.UserAgent().random
    header = { 'user-agent': user }
    proxy_set = set()

    def parser(self, link):
        print(f"Просматриваем ресурс {link}...")
        response = requests.get(link, headers=self.header).text
        self.proxy_set = response.strip().split('\r\n')

        # with open ('result.txt', "w") as file:
        #     file.write("")
        
        print("Информация собрана, начинаем валидацию.\nДоступные адреса будут записаны в файл...")
        with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
            process.map(self.validate_proxy, list(self.proxy_set))

    def validate_proxy(self, proxy):
        link = "https://icanhazip.com/"
        proxies = {
            'http': f"http://{proxy}",
            'https': f"http://{proxy}"
        }

        try:
            response = requests.get(link, proxies=proxies, timeout=2).text
            print(f"{proxy} ✅")
            self.add_proxy_to_file(proxy)
        except:
            print(f"Прокси {proxy} не валидный!")
    
    def add_proxy_to_file(self, proxy):
        with open ('result.txt', "a") as file:
            file.write(f"{proxy}\n")

    def clear_result_file(self):
        with open ('result.txt', "w") as file:
            file.write("")