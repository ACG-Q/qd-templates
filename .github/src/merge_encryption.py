import base64
import json
import time
import os

har_dir = "./har"  # 确保这里的值是一个字符串
with open('tpls_history.json', 'r', encoding='utf8') as f:
    hfile = json.loads(f.read())
    for name, har_data in list(hfile['har'].items()):
        har_file = os.path.join(har_dir, har_data['filename'])
        with open(har_file, 'rb') as f:
            har_content = f.read()
            json_content = json.loads(har_content)
            hfile['har'][name]['content'] = base64.b64encode(json.dumps(json_content, ensure_ascii=False).encode('utf8')).decode('utf8')
    hfile['version'] = time.strftime('%Y%m%d', time.localtime())
json.dump(hfile, open('tpls_history.json', 'w', encoding='utf8'), indent=4, ensure_ascii=False)