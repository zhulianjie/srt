# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5
import sys
import srt

srcSRT = sys.argv[1];
desSRT = sys.argv[1] + ".cn";

print(srcSRT);
print(desSRT);

# Set your own appid/appkey.
appid = '20240630002088542'
appkey = 'z8n6f4Tmt16XzrHhjZw2'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'jp'
to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

with open(srcSRT, 'r', encoding='utf-8') as file:
 	content = file.read();

lines = list(srt.parse(content));

limit = int(sys.argv[2])
print("line limit " + str(limit))

for i in range(len(lines)):
    query = lines[i].content;

    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)

    print("line " + str(i));

    result = r.json()

    # Show response
    lines[i].content = result['trans_result'][0]['dst']

    if (i >= limit):
        break;

print("here");
with open(desSRT, 'w', encoding='utf-8') as file:
    file.write(srt.compose(lines))
