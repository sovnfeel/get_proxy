import requests
import fake_useragent
import multiprocessing
from bs4 import BeautifulSoup
from src.parse_proxy import ParseProxy

class ParseProxyTable(ParseProxy):
    def parser(self, link, table_class_name, td_ip_number = 0, td_port_number = 1):
        print(f"Просматриваем ресурс {link}...")
        get_value = self.parse_page_table(link, table_class_name)
        self.handler(td_ip_number, td_port_number, get_value)

        print("Начинаем валидацию. Доступные адреса будут записаны в файл...")
        with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
            process.map(self.validate_proxy, list(self.proxy_set))

    def parse_page_table(self, link, table_class_name):
        print(f"Начинаем собирать информацию...")
        response = requests.get(link, headers=self.header).text
        
        soup = BeautifulSoup(response, 'lxml')

        block_values = soup.find('div', class_ = table_class_name).find('table').find('tbody')
        get_value = block_values.find_all('tr')
        
        return get_value
        
    def handler(self, td_ip_number, td_port_number, value):
        
        for v in value:
            current_v = v.find_all('td')

            get_connection_info = self.get_connection_info(current_v, td_ip_number, td_port_number)
            get_ip = get_connection_info.get("get_ip")
            get_port = get_connection_info.get("get_port")

            self.proxy_set.add(f"{get_ip}:{get_port}")

    def get_connection_info(self, current_v, td_ip_number, td_port_number):
        get_ip = current_v[td_ip_number].text
        get_port = current_v[td_port_number].text

        return {
            "get_ip": get_ip,
            "get_port": get_port
        }