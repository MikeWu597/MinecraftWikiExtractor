import json
import os

# 配置参数
INPUT_JSON_PATH = "titles.json"  # 输入的JSON文件路径
OUTPUT_DIR = "groups"  # 输出文件夹路径
GROUP_SIZE = 500  # 每组包含的字符串数量


def split_and_save_titles():
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 读取输入的JSON文件
    with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
        titles = json.load(f)  # 假设JSON是一个列表

    # 计算需要分割的组数
    total_titles = len(titles)
    num_groups = (total_titles + GROUP_SIZE - 1) // GROUP_SIZE  # 向上取整

    print(f"总标题数量：{total_titles}，每组 {GROUP_SIZE} 个，共 {num_groups} 组")

    # 分割并保存到多个文件
    for i in range(num_groups):
        start_index = i * GROUP_SIZE
        end_index = min((i + 1) * GROUP_SIZE, total_titles)
        group_titles = titles[start_index:end_index]

        # 生成输出文件名
        output_file = os.path.join(OUTPUT_DIR, f"title{i + 1}.json")

        # 写入到JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(group_titles, f, ensure_ascii=False, indent=2)

        print(f"已保存 {output_file}，包含 {len(group_titles)} 个标题")


if __name__ == "__main__":
    split_and_save_titles()