import requests
import fake_useragent
import multiprocessing
from bs4 import BeautifulSoup
from validate import validate_proxy

link = "https://proxyfreeonly.com/ru/free-proxy-list?protocols=http"

user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}


def parse_page_table(*, page_number: int) -> list:
    response = requests.get(f"{link}&page={page_number}", headers=header).text
    soup = BeautifulSoup(response, 'lxml')

    block_values = soup.find('div', class_ = "style_list__e4Th8").find('table').find('tbody')
    get_value = block_values.find_all('tr')

    return get_value


def handler(*, value) -> None:
    print(f"Начинаем собирать информацию с {page} страницы...")
    for v in value:
        current_v = v.find_all('td')
        get_ip = current_v[0].text
        get_port = current_v[1].text
        proxy_set.add(f"{get_ip}:{get_port}")
        print(f"Значение {get_ip}:{get_port} успешно обработано!")


if __name__ == "__main__":
    proxy_set = set()

    page = 1
    while True:
        page_table = parse_page_table(page_number=page)
        
        if page_table == []:
            break
        else:
            handler(value=page_table)
            page += 1

    with open ('proxy_list.txt', "w") as file:
            file.write("")

    with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
        process.map(validate_proxy, list(proxy_set))