import requests
import fake_useragent
import multiprocessing
from bs4 import BeautifulSoup
from src.parse_proxy import ParseProxy
from src.parse_table import ParseProxyTable


class ParseProxyPagesTables(ParseProxyTable):
    def parser(self, link, delimitor, table_class_name,
             td_ip_number = 0, td_port_number = 1):
        
        print(f"Просматриваем ресурс {link}...")
        page = 1
        while True:
            get_value = self.parse_page_table(link + delimitor + str(page), table_class_name)

            if self.is_page_empty(get_value):
                break
            else:
                print(f"Начинаем собирать информацию c {page} страницы...")
                self.handler(td_ip_number, td_port_number, get_value)

                page += 1

        print("Информация собрана, начинаем валидацию.\nДоступные адреса будут записаны в файл...")
        with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
            process.map(self.validate_proxy, list(self.proxy_set))
    
    def is_page_empty(self, get_value):
        if get_value == []:
            return True
        else:
            return False

    def parse_page_table(self, link, table_class_name):
        response = requests.get(link, headers=self.header).text
        
        soup = BeautifulSoup(response, 'lxml')

        block_values = soup.find('div', class_ = table_class_name).find('table').find('tbody')
        get_value = block_values.find_all('tr')
        
        return get_value
