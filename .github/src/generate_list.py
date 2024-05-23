import json
import os

# 假设tpls_history_with_create_date.json文件位于同一目录下
with open('tpls_history_with_create_date.json', 'r', encoding="utf8") as json_file:
    jsonData = json.load(json_file)

# 创建Markdown文件的路径
list_path = 'LIST.md'

# 创建表格内容
markdown_content = '# 模板历史\n\n'
markdown_content += '| 应用名称 | 作者 | URL | 更新 | 评论 | 文件名 | 创建日期 | 更新日期 | 版本 |\n'
markdown_content += '| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n'

for app_name, app_data in jsonData['har'].items():
    # 检查'create_data'和'data'键是否存在于app_data字典中
    create_data = app_data.get('create_date', 'N/A')  # 如果不存在，提供默认值'N/A'
    data = app_data.get('date', 'N/A')  # 如果不存在，提供默认值'N/A'

    # 检查app_data['update']的值，如果为True，则使用'✅'，否则使用'❎'
    update_status = '✅' if app_data['update'] else '❎'

    # 添加行到Markdown内容中
    markdown_content += f"| {app_name} | {app_data['author']} | [URL]({app_data['url']}) | {update_status} | [评论]({app_data['commenturl']}) | {app_data['filename']} | {create_data} | {data} | {app_data['version']} |\n"

# 写入文件
with open(list_path, 'w', encoding="utf8") as list_file:
    list_file.write(markdown_content)
