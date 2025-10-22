import requests
import re
from requests.exceptions import RequestException
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    response = requests.get('https://news.ycombinator.com', verify=False, timeout=10) #подставляем свой сайт
    html = response.text
except RequestException as e:
    print(f"Не удалось загрузить страницу: {e}")
    exit(1)


links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
if not links:
    print("Ссылки не найдены.")
    exit(0)

print(f"Найдено {len(links)} внешних ссылок. Проверяем...")


bad_links = {}

for i, url in enumerate(links, 1):
    try:

        resp = requests.head(url, timeout=5, allow_redirects=True)
        status = resp.status_code
    except RequestException:

        status = "Connection error"

    if status != 200:
        bad_links[url] = status

    print(f"[{i}/{len(links)}] Проверено: {url} → {status}")


print("\n" + "="*50)
print(f"Проверено {len(links)} ссылок. Найдено {len(bad_links)} битых:")
for url, code in bad_links.items():
    print(f"- {url} → {code}")
