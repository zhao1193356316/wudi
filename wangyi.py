import requests

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
}
req = requests.post(url, headers)
print(req.json())
req.close()
