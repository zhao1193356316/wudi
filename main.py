import requests

url = 'https://weibo.com/ajax/side/hotSearch'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}
req = requests.get(url=url, headers=headers)

re = req.json()['data']['realtime']
sum_ = 0
for i in re:
    print('热搜第', sum_ + 1, ' ', re[sum_]['note'], end=' ')
    print(re[sum_]['num'])
    sum_ += 1
req.close()
