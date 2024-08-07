# proxyChecker.py
import requests

proxyList = [
    "dzqopjfj:y00oudxqek2u@45.127.248.127:5128",
    "dzqopjfj:y00oudxqek2u@64.64.118.149:6732",
    "dzqopjfj:y00oudxqek2u@157.52.253.244:6204",
    "dzqopjfj:y00oudxqek2u@167.160.180.203:6754",
    "dzqopjfj:y00oudxqek2u@166.88.58.10:5735",
    "dzqopjfj:y00oudxqek2u@173.0.9.70:5653",
    "dzqopjfj:y00oudxqek2u@45.151.162.198:6600",
    "dzqopjfj:y00oudxqek2u@204.44.69.89:6342",
    "dzqopjfj:y00oudxqek2u@173.0.9.209:5792",
    "dzqopjfj:y00oudxqek2u@206.41.172.74:6634",
]

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

def get_working_proxy():
    """Повертає перший робочий проксі з списку."""
    for proxy_candidate in proxyList:
        if check_proxy(proxy_candidate):
            return proxy_candidate
    return None
