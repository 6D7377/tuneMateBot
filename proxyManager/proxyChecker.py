# proxyChecker.py
import requests

def load_proxies_from_file(filename):
    """Читає список проксі з файлу."""
    with open(filename, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def check_proxy(proxy):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_working_proxy(proxy_list):
    """Повертає перший робочий проксі з списку."""
    for proxy_candidate in proxy_list:
        if check_proxy(proxy_candidate):
            return proxy_candidate
    return None

def main():
    proxy_list = load_proxies_from_file('proxy.txt')
    working_proxy = get_working_proxy(proxy_list)
    if working_proxy:
        print(f"Робочий проксі: {working_proxy}")
    else:
        print("Не знайдено робочих проксі.")

if __name__ == "__main__":
    main()
