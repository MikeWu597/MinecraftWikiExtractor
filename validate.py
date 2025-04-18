import os
import json
import re

# 定义文件路径
titles_file = "titles.json"
res_folder = "res"
missing_file = "titles_missing.json"

def sanitize_filename(title):
    """清理文件名中的非法字符"""
    # 保留字母数字和中文，替换其他字符为下划线
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', title)
    # 替换连续下划线为单个
    return re.sub(r'_+', '_', sanitized).strip('_')

# 读取 titles.json 文件
with open(titles_file, "r", encoding="utf-8") as f:
    titles = json.load(f)

# 获取 res 文件夹中的所有文件名（去掉扩展名）
res_files = {os.path.splitext(file)[0] for file in os.listdir(res_folder) if file.endswith(".txt")}

# 找出 titles 中没有对应文件的名称
missing_titles = [title for title in titles if sanitize_filename(title) not in res_files]

# 将缺失的名称写入 titles_missing.json 文件
with open(missing_file, "w", encoding="utf-8") as f:
    json.dump(missing_titles, f, ensure_ascii=False, indent=4)

print(f"Missing titles have been saved to {missing_file}")
