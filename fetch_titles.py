import time
import random
from curl_cffi import requests  # 需要安装：pip install curl_cffi

API_URL = 'https://zh.minecraft.wiki/api.php'

def fetch_all_titles():
    all_titles = []
    params = {
        'action': 'query',
        'format': 'json',
        'assert': 'anon',
        'generator': 'allpages',
        'gaplimit': 'max',
        'formatversion': 2
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://zh.minecraft.wiki/',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'TE': 'Trailers'
    }

    retry_count = 0
    max_retries = 5

    while True:
        try:
            # 使用curl_cffi发送请求，模拟Chrome 120的TLS指纹
            response = requests.get(
                API_URL,
                params=params,
                headers=headers,
                impersonate='chrome120',  # 关键：模拟浏览器TLS指纹
                timeout=20
            )
            response.raise_for_status()
            data = response.json()

        except requests.HTTPError as e:
            print(f"请求失败（错误类型：{type(e).__name__}）：{e}")
            retry_count += 1
            if retry_count >= max_retries:
                print("超过最大重试次数，终止请求")
                break
            wait_time = 2 ** retry_count
            time.sleep(wait_time)
            continue

        # 提取当前页标题
        pages = data.get('query', {}).get('pages', [])
        if not pages:
            break
        all_titles.extend(page['title'] for page in pages)

        # 处理分页参数（注意使用 `gapcontinue`）
        if 'continue' in data:
            params['gapcontinue'] = data['continue']['gapcontinue']
        else:
            break

        # 随机等待5~15秒（降低请求频率）
        time.sleep(1)

    return all_titles

def save_titles_to_file(titles, filename='titles.txt'):
    formatted_titles = '","'.join(titles)
    output = f'"{formatted_titles}"' if formatted_titles else ''

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(output)

if __name__ == '__main__':
    print("正在获取所有页面标题...")
    titles = fetch_all_titles()
    print(f"共获取到 {len(titles)} 个页面标题")

    if titles:
        save_titles_to_file(titles)
        print("标题已保存到 titles.txt 文件")
    else:
        print("未获取到任何标题，请检查网络或参数设置")
