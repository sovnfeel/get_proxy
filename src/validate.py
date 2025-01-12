import requests
import multiprocessing


def validate_proxy(proxy):
    link = "https://icanhazip.com/"
    
    proxies = {
        'http': f"http://{proxy}",
        'https': f"http://{proxy}"
    }

    try:
        response = requests.get(link, proxies=proxies, timeout=2).text
        print(proxy)
        with open ('proxy_list.txt', "a") as file:
            file.write(f"{proxy}\n")
    except:
        print(f"Прокси {proxy} не валидный!")