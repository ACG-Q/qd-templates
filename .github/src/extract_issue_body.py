import base64
import json
import os
import time

# 读取tpls_history.json文件
with open('tpls_history.json', 'r', encoding='utf8') as f:
    hfile = json.load(f)

# 从环境变量获取issue数据
issue_body = os.getenv('ISSUE_JSON', '{}')
issue_json = json.loads(issue_body)

repo_full_name = os.getenv('REPO_FULL_NAME', '')
repo_default_branch = os.getenv('REPO_DEFAULT_BRANCH', '')

# 设置har保存文件夹
har_dir = "har"

# 检查issue_json是否包含必要的字段
if issue_json and 'name' in issue_json and 'author' in issue_json and 'filename' in issue_json and 'har_content' in issue_json:
    commenturl = os.getenv('ISSUE_URL', '')
    issue_json['name'] = issue_json['name'].replace(' ', '_')
    issue_json['filename'] = issue_json['filename'].replace(' ', '_')

    # 处理har内容
    har_content = issue_json['har_content'].replace('```JSON', '').replace('```', '').strip()
    try:
        har_content = json.loads(har_content)
    except:
        os._exit(0)

    update = False

    # 检查hfile中是否存在对应的记录
    if 'har' not in hfile or not isinstance(hfile['har'], dict):
        hfile['har'] = {}
    elif issue_json['name'] in hfile['har']:
        update = True
    else:
        for k, v in list(hfile['har'].items()):
            if v['commenturl'] == commenturl:
                hfile['har'][issue_json['name']] = v
                update = True
                hfile['har'].pop(k)
                break

    # 处理filename
    if not issue_json['filename']:
        issue_json['filename'] = issue_json['name'] + '.har'
    if not issue_json['filename'].endswith('.har'):
        issue_json['filename'] = issue_json['filename'] + '.har'

    # 删除旧文件
    if update and issue_json['filename'] != hfile['har'][issue_json['name']]['filename'] and os.path.exists(hfile['har'][issue_json['name']]['filename']):
        os.remove(hfile['har'][issue_json['name']]['filename'])
        
    # 生成保存文件路径
    har_file = os.path.join(har_dir, issue_json['filename'])

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(har_dir):
        try:
            os.mkdir(har_dir)
        except OSError as e:
            print(f"Failed to create directory {har_dir}: {e}")


    # 写入新文件
    with open(har_file, 'w', encoding='utf8') as f:
        f.write(json.dumps(har_content, indent=4, ensure_ascii=False))

    # 构建har对象
    har = {
        'name': issue_json['name'],
        'author': issue_json['author'],
        'url': f'https://raw.githubusercontent.com/{repo_full_name}/{repo_default_branch}/{har_file}',
        'update': update,
        'comments': issue_json.get('comments', '').replace('\\r', '\r').replace('\\n', '\n').replace('\r', '').replace(
            '\n', '<br>').strip(),
        'filename': issue_json['filename'],
        'content': base64.b64encode(json.dumps(har_content, ensure_ascii=False).encode('utf8')).decode('utf8'),
        'date': hfile['har'][issue_json['name']]['date'] if update else time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                        time.localtime()),
        'version': hfile['har'][issue_json['name']]['version'] if update else time.strftime('%Y%m%d',
                                                                                                time.localtime()),
        'commenturl': commenturl
    }

    # 更新hfile['har'][issue_json['name']]
    if not hfile['har'].get(issue_json['name']):
        hfile['har'][issue_json['name']] = har
    elif update and hfile['har'][issue_json['name']] != har:
        hfile['har'][issue_json['name']] = har
        hfile['har'][issue_json['name']]['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        hfile['har'][issue_json['name']]['version'] = time.strftime('%Y%m%d', time.localtime())

    # 更新tpls_history.json文件
    with open('tpls_history.json', 'w', encoding='utf8') as f:
        json.dump(hfile, f, indent=4, ensure_ascii=False)
