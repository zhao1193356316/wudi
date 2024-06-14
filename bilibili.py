import os

import requests
import re
import json
import subprocess
from DrissionPage import ChromiumPage

headers = {
    'Cookie': 'buvid3=3532825D-2661-42B9-76A2-5DFAB7E6216474776infoc; b_nut=1717155174; CURRENT_FNVAL=4048; _uuid=DA254BD5-E12E-B2B1-AE17-A844A352B8BB76122infoc; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTc0MTQzNzUsImlhdCI6MTcxNzE1NTExNSwicGx0IjotMX0.0npLWP67kw8GQYKxSAJXi8vL8GBm8l8zG5RDERN3RYk; bili_ticket_expires=1717414315; buvid_fp=727687b4bc974400d0b06e35549ec740; buvid4=EA8BCFA1-D815-B908-27D8-3FDDA43F439B75821-024053111-E7Pq0MaqJKOXc3NTFqMfOA%3D%3D; rpdid=|(k|Y~|RYk)J0J\'u~u~ullu~Y; b_lsid=79B44249_18FD16AE70B; SESSDATA=1d644684%2C1732758284%2C41618%2A61CjDhnZFCMk-ymLSb9hNMTyA_Pv93UpEoVQxooZutpOAZnj6VIrzSpiaUOq89UrqCMuYSVmFCby1USVdZTk12T1JOZktRd2hCN0VMSVFWdDdXVDZGeHBsbDgwM0hKWXdtYW9WT0JEUktyTTZvT0lnYTZwdDdZQ25qQXc1bDhOWllVNy13cnJzYUVnIIEC; bili_jct=25aa10727a9ac87bde2c8725c03b8675; DedeUserID=2013824685; DedeUserID__ckMd5=9c98eb011f51a7e7; sid=hhz5ycgj',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/?spm_id_from=333.788.0.0'
}


def Gethtml(url):
    req = requests.get(url, headers=headers)
    return req


def Getlinjie(bv):
    url = f'https://www.bilibili.com/video/{bv}/?spm_id_from=333.1007'
    html = Gethtml(url).text
    link = re.findall('<script>window.__playinfo__=(.*?)</script>', html)[0]
    title = re.findall('<h1 data-title="(.*?)"', html)[0]
    audio_url = json.loads(link)['data']['dash']['audio'][0]['baseUrl']
    video_url = json.loads(link)['data']['dash']['video'][0]['baseUrl']
    return title, audio_url, video_url


def Save(title, audio_url, video_url):
    # 获取音频和视频内容
    audio_content = Gethtml(audio_url).content
    video_content = Gethtml(video_url).content
    # 创建保存目录
    save_dir = 'void'
    os.makedirs(save_dir, exist_ok=True)
    # 文件路径
    audio_path = os.path.join(save_dir, title + '.mp3')
    video_path = os.path.join(save_dir, title + '.mp4')
    output_path = os.path.join(save_dir, title + '_merged.mp4')
    print(audio_path)
    print(video_path)
    # 保存音频文件
    with open(audio_path, mode='wb') as f:
        f.write(audio_content)
    # 保存视频文件
    with open(video_path, mode='wb') as f:
        f.write(video_content)
    # 合并音频和视频
    cmp = f"ffmpeg -hide_banner -i \"{video_path}\" -i \"{audio_path}\" -c:v copy -c:a aac -strict experimental \"{output_path}\""
    subprocess.run(cmp, shell=True, check=True)
    # 删除原始音频和视频文件
    os.remove(audio_path)
    os.remove(video_path)
    print('保存完成')


if __name__ == '__main__':
    chrom = ChromiumPage()
    chrom.listen.start('api.bilibili.com/x/space/wbi/arc/search')
    chrom.get('https://space.bilibili.com/18337466/video')
    json_ = chrom.listen.wait()
    Data = json_.response.body
    print(Data)
    for index in Data['data']['list']['vlist']:
        bv = index['bvid']
        title, audio_url, video_url = Getlinjie(bv)
        print(title, bv)
        Save(title, audio_url, video_url)
