import json
import os

# 读取tpls_history.json文件
with open('tpls_history.json', 'r', encoding='utf8') as f:
    hfile = json.load(f)

# 从环境变量获取issue数据
issue_body = os.getenv('ISSUE_JSON', '{}')
issue_json = json.loads(issue_body)

# 检查issue_json是否包含必要的字段
if not issue_json or 'name' not in issue_json or 'filename' not in issue_json:
    print('False')
else:
    commenturl = os.getenv('ISSUE_URL', '')
    issue_json['name'] = issue_json['name'].replace(' ', '_')
    issue_json['filename'] = issue_json['filename'].replace(' ', '_')
    filename = issue_json['filename']
    issue_already_recorded = False

    # 检查hfile中是否存在对应的记录
    for k, v in list(hfile.get('har', {}).items()):
        if v.get('commenturl') == commenturl or issue_json['name'] == k:
            issue_already_recorded = True
            if filename != v['filename'] and os.path.exists(v['filename']):
                os.remove(v['filename'])
            hfile['har'].pop(k, None)
            break

    # 删除文件
    if os.path.exists(filename):
        os.remove(filename)

    # 如果记录已存在，则更新tpls_history.json文件
    if issue_already_recorded:
        with open('tpls_history.json', 'w', encoding='utf8') as f:
            json.dump(hfile, f, indent=4, ensure_ascii=False)
        print('True')
    else:
        print('False')
