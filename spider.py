import json
import time
import random
import os
import certifi
import re
from urllib.parse import quote
from curl_cffi import requests
from bs4 import BeautifulSoup
from bs4 import Comment

# 配置参数
MEDIAWIKI_BASE_URL = "https://zh.minecraft.wiki/w/"
INPUT_JSON_PATH = "groups/title7.json"
OUTPUT_DIR = "out7"


def sanitize_filename(title):
    """清理文件名中的非法字符"""
    # 保留字母数字和中文，替换其他字符为下划线
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', title)
    # 替换连续下划线为单个
    return re.sub(r'_+', '_', sanitized).strip('_')


def html_to_text(html_content):
    """改进版HTML转文本处理"""
    soup = BeautifulSoup(html_content, 'html.parser')
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()  # 删除注释节点
    # 移除不需要的元素
    [tag.decompose() for tag in soup(['script', 'style', 'head', 'nav', 'footer', 'img'])]

    # 处理主要内容区域
    content_div = soup.find('div', {'id': 'mw-content-text'})
    if not content_div:
        return ""
        # 移除特定的调试信息和元信息


    for element in content_div.find_all(['div', 'p']):
        text = element.get_text(strip=True)
        if any(keyword in text for keyword in [
            "Parsed by mediawiki",
            "Cached time:",
            "Cache expiry:",
            "CPU time usage:",
            "Real time usage:",
            "Preprocessor visited node count:",
            "Post-expand include size:",
            "Template argument size:",
            "Highest expansion depth:",
            "Expensive parser function count:",
            "Unstrip recursion depth:",
            "Unstrip post-expand size:",
            "ExtLoops count:",
            "Lua time usage:",
            "Lua memory usage:",
            "Transclusion expansion time report",
            "取自"
        ]):
            element.decompose()
    text = []
    for element in content_div.descendants:
        if isinstance(element, str):
            stripped = element.strip()
            if stripped:
                text.append(stripped)
        elif element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            text.append(f"\n\n{'#' * int(element.name[1])} {element.get_text(strip=True)}\n")
        elif element.name == 'p':
            text.append(element.get_text(separator='', strip=True))
        elif element.name == 'li':
            text.append(f"\n- {element.get_text(strip=True)}")

    return ''.join(text).strip()


def fetch_page_content(title):
    """使用curl_cffi获取页面内容"""
    url = f"{MEDIAWIKI_BASE_URL}{quote(title)}"

    try:
        response = requests.get(
            url,
            impersonate="chrome110",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            },
            timeout=15,
            verify="cacert.pem"
        )

        if response.status_code == 200:
            return response.text
        else:
            print(f"HTTP Error {response.status_code} for {title}")
            return None
    except Exception as e:
        print(f"Error fetching {title}: {str(e)}")
        return None


def main():
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 读取标题列表
    with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
        titles = json.load(f)

    total = len(titles)

    for i, title in enumerate(titles, 1):
        print(f"Processing {i}/{total}: {title}")
        html = fetch_page_content(title)

        if html:
            text = html_to_text(html)
            #text = html
            # 生成安全的文件名
            safe_filename = sanitize_filename(title)
            file_path = os.path.join(OUTPUT_DIR, f"{safe_filename}.txt")

            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text or "无法提取内容")

            print(f"Saved to {file_path}")

        # 随机延迟3-10秒
        if i < total:
            delay = random.uniform(1, 5)
            print(f"等待 {delay:.2f} 秒...")
            time.sleep(delay)

    print(f"完成！所有文件已保存到 {OUTPUT_DIR} 目录")


if __name__ == "__main__":
    main()