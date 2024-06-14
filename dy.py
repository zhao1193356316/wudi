import asyncio
import aiofiles
import aiohttp
from DrissionPage import ChromiumPage

Datalist = []


def getlist(cookies, url):
    Chrom = ChromiumPage()
    Chrom.listen.start('https://www.douyin.com/aweme/v1/web/aweme/post/')
    Chrom.get(url)
    Chrom.set.cookies(cookies)
    for packet in Chrom.listen.steps(timeout=10):
        print(packet.url)  # 打印数据包url
        Chrom.scroll.to_bottom()  # 点击下一页
        Datalist.append(packet)
    Chrom.close()


async def getTheDownloadLink():
    async with aiohttp.ClientSession() as sess:
        tasks = []
        for packet in Datalist:
            Datalink = packet.response.body['aweme_list']
            for i in Datalink:
                title = i['desc'].replace('\n', ' ')
                link = i['video']['play_addr']['url_list'][0]
                task = asyncio.ensure_future(download_file(title, link, sess))
                tasks.append(task)
            await asyncio.wait(tasks)


async def download_file(title, link, sess):
    async with sess.get(link) as resp:
        async with aiofiles.open(f'void3/{title}.mp4', mode='wb') as f:
            await f.write(await resp.content.read())
            print(f'{title}：保存成功')


if __name__ == '__main__':
    # 自己的cookie
    cookies = 'ttwid=1%7CW5Jq2623jIjZFOUwYEOpeoRwlavkbVkt9fgtgFElC0w%7C1718112106%7Cb5c34e6ebd4884916523c69bbd1e3dc89b620a9fa6d016eadf1eccdf5ba50707; dy_swidth=1536; dy_sheight=864; s_v_web_id=verify_lxafl7ig_ErwaP1rD_V1fe_4rHu_BGvF_yw2RR2uYVr0W; passport_csrf_token=278295e9ab77abc4b08ba84f03d8904a; passport_csrf_token_default=278295e9ab77abc4b08ba84f03d8904a; bd_ticket_guard_client_web_domain=2; xgplayer_user_id=480657737764; download_guide=%223%2F20240613%2F0%22; pwa2=%220%7C0%7C3%7C0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; passport_assist_user=CkAThR2ryRzo0b7WE1Pu-AttJiXklOCky36LLvASSrBhsZIJwGgwpb2aJOWA2KpLO9FI-J63umaEzptwjejaLSXRGkoKPMspELM32PAS3mOhlNhwvOJsDhC7HbZxW0EUs0MfPqKS-movAnF_VGBFMFj0CIXNSjIg2Y1isOG9Oju3VRDw9NMNGImv1lQgASIBAzo3WxI%3D; n_mh=036aAHGVRZ8Exi-Zq_xyEd2vWjU4rrtnWQUpl7hZd14; sso_uid_tt=62eb669af2001772cfada25e2e80b165; sso_uid_tt_ss=62eb669af2001772cfada25e2e80b165; toutiao_sso_user=f9dcc5beb77c3cf73e38d393fdca9b58; toutiao_sso_user_ss=f9dcc5beb77c3cf73e38d393fdca9b58; sid_ucp_sso_v1=1.0.0-KGIwMjRhZGI4MGI5MDk2ZGZkNTdjZDI2NjlhYzc2MmJhNDljYjNlN2MKIQiO44DG3vTZARDU9KqzBhjvMSAMMNyc-vIFOAZA9AdIBhoCbGYiIGY5ZGNjNWJlYjc3YzNjZjczZTM4ZDM5M2ZkY2E5YjU4; ssid_ucp_sso_v1=1.0.0-KGIwMjRhZGI4MGI5MDk2ZGZkNTdjZDI2NjlhYzc2MmJhNDljYjNlN2MKIQiO44DG3vTZARDU9KqzBhjvMSAMMNyc-vIFOAZA9AdIBhoCbGYiIGY5ZGNjNWJlYjc3YzNjZjczZTM4ZDM5M2ZkY2E5YjU4; passport_auth_status=56fd1b0d2c8a7dd1b0c997e7f12203a3%2C; passport_auth_status_ss=56fd1b0d2c8a7dd1b0c997e7f12203a3%2C; uid_tt=26e5ed25a8827d9654647d0226bfce7b; uid_tt_ss=26e5ed25a8827d9654647d0226bfce7b; sid_tt=b3a0beb8f36be0e6f3be9808bc50b7e9; sessionid=b3a0beb8f36be0e6f3be9808bc50b7e9; sessionid_ss=b3a0beb8f36be0e6f3be9808bc50b7e9; publish_badge_show_info=%220%2C0%2C0%2C1718270558676%22; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=4b892cdf3773257346d527e7b2784e53; __security_server_data_status=1; sid_guard=b3a0beb8f36be0e6f3be9808bc50b7e9%7C1718270560%7C5183991%7CMon%2C+12-Aug-2024+09%3A22%3A31+GMT; sid_ucp_v1=1.0.0-KDc0NjQ0YzUwYTZmOGIzZGZhNDcxZmU4NDkxZjg5M2U4NWM1YTQxMjAKGwiO44DG3vTZARDg9KqzBhjvMSAMOAZA9AdIBBoCaGwiIGIzYTBiZWI4ZjM2YmUwZTZmM2JlOTgwOGJjNTBiN2U5; ssid_ucp_v1=1.0.0-KDc0NjQ0YzUwYTZmOGIzZGZhNDcxZmU4NDkxZjg5M2U4NWM1YTQxMjAKGwiO44DG3vTZARDg9KqzBhjvMSAMOAZA9AdIBBoCaGwiIGIzYTBiZWI4ZjM2YmUwZTZmM2JlOTgwOGJjNTBiN2U5; store-region=cn-ha; store-region-src=uid; __ac_signature=_02B4Z6wo00f01ebXq7QAAIDAOq40Ay0Gn7Hm968AAB.h32; my_rd=2; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; WallpaperGuide=%7B%22showTime%22%3A1718270597852%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A19%2C%22cursor2%22%3A0%7D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA9amzI2Qt2sHQSEQkyiPcUQik5hb99vc3QKdlhAaJKCk%2F1718294400000%2F0%2F0%2F1718279318813%22; douyin.com; xg_device_score=7.802204888412783; device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64; home_can_add_dy_2_desktop=%220%22; csrf_session_id=9859fbbaa24fd7d943872d675196cac7; strategyABtestKey=%221718326812.124%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA9amzI2Qt2sHQSEQkyiPcUQik5hb99vc3QKdlhAaJKCk%2F1718380800000%2F0%2F1718326812204%2F0%22; IsDouyinActive=true; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCS2lJcktDWmM0eHdTOWR1V2ZIVW41aUZuenVwNUpVOHpaMGlRbG43QzhscnNYVWJOdWdhRzZlQWZJc3k2Vm5NMkJMTXJoVEoyUWUzUGo5WEU3REdIVW89IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; odin_tt=34b85ebebde73b7f179dc3b15bb08ceadce0b7bb2b9c97ebeade87add50d6c983b4109dfa40d9c6add36fb060c30a880f934116d20e52a89d9cc96c33ecd9adf; passport_fe_beating_status=true; msToken=NqGVFwHbD_HaORQrr82mKcH1BnnjMQuA62ypHj7Cby__cYKUfiQnTiZBt8QO90DARFdYiTOgqWBdkxRm6II2V1ZmRjo0Gbi-lrrgQmm6dRVbN7OoIyXX'
    # 要下载视频的博主首页url
    url = 'https://www.douyin.com/user/MS4wLjABAAAAYOE9rmlF0BK1SfWebikMkKVSV-DjwVukQL_8tC5FMLA?vid=7372433407613111571'
    getlist(cookies, url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getTheDownloadLink())
