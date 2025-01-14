from src.parse_proxy import ParseProxy
from src.parse_table import ParseProxyTable
from src.multiple_tables import ParseProxyPagesTables


def main():
    proxy_lis = ParseProxy()
    free_proxy_list = ParseProxyTable()
    free_proxy_only = ParseProxyPagesTables()

    proxy_lis.clear_result_file()
    
    proxy_lis.parser("https://www.proxy-list.download/api/v1/get?type=http")
    free_proxy_list.parser("https://free-proxy-list.net/", "table-responsive")
    free_proxy_only.parser("https://proxyfreeonly.com/ru/free-proxy-list?protocols=http",
                        "&page=", "style_list__e4Th8")

    print("Сохранено в файл result.txt")

if __name__ == "__main__":
    main()