import requests

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}


def Gethtml(url):
    req = requests.get(url=url, headers=headers)
    return req


if __name__ == '__main__':
    # url = 'https://s8.fsvod1.com/20230503/8JwJpBcY/1500kb/hls/index.m3u8'
    url='https://yhdm6.top/index.php/vod/play/id/17344/sid/6/nid/2/'
    html = Gethtml(url).text
    print(html)
    # with open('zhetian.ts', mode='wb') as f:
    #     f.write(html)


'''

https://s8.fsvod1.com/20230503/8JwJpBcY/index.m3u8
https://s8.fsvod1.com/20230503/8JwJpBcY/1500kb/hls/index.m3u8


8JwJpBcY
qKUsMq3G
集数id
https://s8.fsvod1.com/20230503/qKUsMq3G/index.m3u8
https://s8.fsvod1.com/20230503/qKUsMq3G/1500kb/hls/index.m3u8






'''