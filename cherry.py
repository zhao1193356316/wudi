from DrissionPage import ChromiumPage
import requests
import asyncio
import aiohttp
import aiofiles

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}


def Drp(url):
    chrom = ChromiumPage()
    chrom.get(url)
    iframe = chrom.ele('xpath://*[@id="playleft"]/iframe')
    iframe_Src = iframe.attr('src')
    chrom.close()
    m3u81 = iframe_Src.split('&url=')[1]
    return m3u81


def getreq(url):
    req = requests.get(url, headers)
    return req


def getVideoLink(m3u81):
    contents = getreq(m3u81).text
    contents = contents.strip()
    m3u8_list = []
    title_list = []
    for line in contents.split('\n'):
        if line.startswith('#'):
            continue
        m3u82 = line
    m3u82 = m3u81.replace('index.m3u8', m3u82)
    m3u82_contents = getreq(m3u82).text
    m3u82_contents = m3u82_contents.strip()
    for line in m3u82_contents.split('\n'):
        if line.startswith('#'):
            continue
        title = line
        m3u82_link = m3u82.replace('mixed.m3u8', title)
        title_list.append(title)
        m3u8_list.append(m3u82_link)
    return m3u8_list, title_list


async def download_file(sess, link, title):
    async with sess.get(link) as resp:
        async with aiofiles.open(f'void2/{title}', mode='wb') as f:
            await f.write(await resp.content.read())
            print(f'{title}：保存成功')


async def downloadTheVideo(m3u8_list, title_list):
    async with aiohttp.ClientSession() as sess:
        tasks = []
        for link in m3u8_list:
            task = asyncio.ensure_future(download_file(sess, link, title_list[a]))
            tasks.append(task)
        await asyncio.wait(tasks)


if __name__ == '__main__':
    url = 'https://yhdm6.top/index.php/vod/play/id/17344/sid/6/nid/60/'
    m3u81 = Drp(url)
    m3u8_list, title_list = getVideoLink(m3u81)
    print(m3u8_list)
    print(title_list)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(downloadTheVideo(m3u8_list, title_list))
    loop.run_until_complete(asyncio.ensure_future(downloadTheVideo(m3u8_list, title_list)))
    print('保存成功')
