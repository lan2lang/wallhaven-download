import json
from io import BytesIO

import aiohttp
import asyncio

import requests
from fake_useragent import UserAgent
from datetime import datetime
from bs4 import BeautifulSoup
import os
import time
import imghdr
from PIL import Image

count = 0
fail_count=0


# 异步下载文件函数
async def download_file(session, url, file_name, header):
    async with session.get(url, ssl=False, headers=header) as response:
        global count,fail_count
        # print(header)
        content = await response.read()
        image_stream = BytesIO(content)

        try:
            # 尝试打开图片流
            Image.open(image_stream)
            with open(file_name, 'wb') as f:
                f.write(content)
            count = count + 1
            print(f"{file_name} 下载完成")
        except Exception:
            print('下载失败:', url)
            with open('fail2.txt','a+') as f:
                f.write(url+"\n")
            fail_count=fail_count+1



async def main():
    # 创建异步会话
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []

        for url in img_urls:
            header = {'User-Agent': ua.random}
            # print(url)
            file_name = dir + url.split('/')[-1]
            # 创建下载任务
            task = download_file(session, url, file_name, header)
            tasks.append(task)

        # 并发执行下载任务
        await asyncio.gather(*tasks)

    print("下载完成！-" + str(count))
    print("失败：-" + str(fail_count))


def str_insert(str_origin, pos, str_add):
    """
    在字符串指定位置插入字符
    str_origin：源字符串  pos：插入位置  str_add：待插入的字符串
    :param str_origin:
    :param pos:
    :param str_add:
    :return:
    """
    str_list = list(str_origin)  # 字符串转list
    str_list.insert(pos, str_add)  # 在指定位置插入字符串
    str_out = ''.join(str_list)  # 空字符连接
    return str_out


if __name__ == '__main__':
    ua = UserAgent()

    imgType_list = {'jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif'}
    # 加上这一行,解决使用代理请求 https会报错问题
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # #解决代理问题
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"

    # 目标网页URLz
    # categories(常规，动漫，人)，purity（健康，亚健康，黄），（1M，1d,1y）过去一个月
    # url = 'https://wallhaven.cc/search?categories=111&purity=001&topRange=6M&sorting=toplist&order=desc&ai_art_filter=0'
    # url = 'https://wallhaven.cc/search?categories=111&purity=011&topRange=3M&sorting=toplist&order=desc&ai_art_filter=1&page=4'
    url = 'https://wallhaven.cc/search?q=id%3A108736&categories=111&purity=011&sorting=relevance&order=desc&ai_art_filter=1&page=15'
    # 图片保存文件夹
    # dir = f'download/{datetime.now().month}_{+datetime.now().day}/'
    dir = f'download/chunmomo/'
    # 下载文件存放目录
    os.makedirs(dir, exist_ok=True)

    # 如果需要下载nsfw，需要添加cookie
    cookie = '_pk_id.1.01b8=9abd6dbf0670cce7.1692106714.; _pk_ses.1.01b8=1; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IkhJUTgrNmc0TUdXR1RpSU56NUs2cWc9PSIsInZhbHVlIjoieTlDQ3FuZDJWeUNwYmxtSE9DQWNcL1A2VE1VOG5iR2FxcEdpeFNkVHQ1Y0pEZWp4NzdQdkI2TStGKyt6UFY3UHFHUGtCRjVPbXVwamlIMUVOZitPMDRCRGRrbk9udWhxa1FxS1ZubFJlSEh4Y0J2clZubVhYRVRwMUI0K2Y3YTg2c3p4VVcxbklWZk1nbmZTeE9XM1dKTll1M3BtTk5wbHNnTEZFZWZOMW1NTURTOFRWMEk3ZU9yZkQzWnNCQnRcL2oiLCJtYWMiOiI1ZWM1NDZhZmQwMzJjY2YyYmRmMmVmMDRjNWIzYWQ5YTllNzA0NzllMjE3YTY5NGNkZGU1MWQ5YTFkNGE3ZTVlIn0%3D; XSRF-TOKEN=eyJpdiI6IkZvbUhNM3dxYmtPSlI3Z2Nxc2FTZEE9PSIsInZhbHVlIjoiY1YwbjVBbWRqZ0pUS3h2SnFuZUtIUWlJaHdZTnkyak4yVzQ1MzNFNEcwZmIzSEM0djN1aFFqOWtTQjB1Z2owTSIsIm1hYyI6ImQyMGRiMmUyMzQ3NzU2ZDE5ODgyOTFiMGNmZjNlM2Y1YWE5YTdkZDE1NmIxZTIxNmI1OTQzYjJkNDc3YjRjNDAifQ%3D%3D; wallhaven_session=eyJpdiI6IkQ4bCtYaFU0citnWFcwdzRUWGZJWVE9PSIsInZhbHVlIjoiK3BpVDZYMHpvYXNZa0puTkU1c28xOXZTSHEyMHpzcW9WdWd0OXJyRkhcLzVocEFrVk51ang2b1wvUThjbitOb29XIiwibWFjIjoiMDQ3NTFkNTk1YWU1ODM2OTNkZGI4Njk3OGVjMTk5MmExNWUxMjk0N2MxYTc2YThmZWNjNWUyOTVkYmQ5ODhmMCJ9'
    cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}

    # 获取网页内容
    resp = requests.get(url, cookies=cookie_dict, headers={'User-Agent': ua.random})
    soup = BeautifulSoup(resp.text, 'html.parser')

    resp.close()

    #清空

    # 获取图片URL列表
    img_urls = []

    for img in soup.find_all('img'):
        img_url = img.get('data-src')
        if img_url is not None:
            img_url = str(img_url).replace('th', 'w', 1).replace('small', 'full', 1)
            img_url = str_insert(img_url, img_url.rfind('/') + 1, 'wallhaven-')
            img_urls.append(str(img_url))
            # img_urls.append(str(img_url)[:-3] + 'png')

    # 运行异步主函数
    asyncio.run(main())
