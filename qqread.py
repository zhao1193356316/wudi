import requests
import re

url = 'https://book.qq.com/book-read/43893441/3'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Referer': 'https://book.qq.com/book-read/48892580/1',
    'Cookie': 'logTrackKey=efa56bb7724844c18b71fb384a1b0c99; secToken=5981157f7a5cfa703cbe5035067fa14a; fuid=29f063735ca24c4bbef1b5087d0d8b96'
}
req = requests.post(url, headers)
html = req.text
content = re.findall(
    '<div id="article" class="chapter-content isTxt" style="font-size:18px;" data-v-27ec98a7>(.*?)</div>', html)[0]
a = 0
line = re.findall('<p>(.*?)</p>', content)
for i in line:
    with open('xiaos.txt', mode='a', encoding='utf-8') as f:
        f.write(line[a])
    a += 1
with open('xiaos.txt', mode='a', encoding='utf-8') as f:
    f.write('\r')
print('保存完成')
