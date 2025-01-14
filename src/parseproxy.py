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




# proxy_lis = ParseProxy()

# proxy_lis.parser("https://www.proxy-list.download/api/v1/get?type=http")


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
            print(f"Значение {get_ip}:{get_port} успешно добавлено!")

    def get_connection_info(self, current_v, td_ip_number, td_port_number):
        get_ip = current_v[td_ip_number].text
        get_port = current_v[td_port_number].text

        return {
            "get_ip": get_ip,
            "get_port": get_port
        }




free_proxy_list = ParseProxyTable()

free_proxy_list.parser("https://free-proxy-list.net/", "table-responsive")


class ParseProxyPagesTables(ParseProxyTable):
    def parser(self, link, delimitor, table_class_name,
             td_ip_number = 0, td_port_number = 1):
        
        print(f"Просматриваем ресурс {link}...")
        page = 1
        while True:
            get_value = self.parse_page_table(link + delimitor + str(page), table_class_name)

            if is_page_empty(get_value):
                break
            else:
                print(f"Начинаем собирать информацию c {page} страницы...")
                self.handler(td_ip_number, td_port_number, get_value)

                page += 1

        print("Начинаем валидацию. Доступные адреса будут записаны в файл...")
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

# free_proxy_only = ParseProxyPagesTables()
# free_proxy_only.parser("https://proxyfreeonly.com/ru/free-proxy-list?protocols=http",
#                     "&page=", "style_list__e4Th8")

