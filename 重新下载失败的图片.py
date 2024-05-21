import asyncio
import os
from io import BytesIO

import requests
from PIL import Image
from fake_useragent import UserAgent

if __name__ == '__main__':
    ua = UserAgent()

    imgType_list = {'jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif'}

    # 加上这一行,解决使用代理请求 https会报错问题
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # #解决代理问题
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"

    # 目标网页URLz
    url = 'https://wallhaven.cc/search?categories=111&purity=110&topRange=1d&sorting=toplist&order=desc&ai_art_filter=1&page=2'

    cookie = '_pk_id.1.01b8=9abd6dbf0670cce7.1692106714.; _pk_ses.1.01b8=1; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IkhJUTgrNmc0TUdXR1RpSU56NUs2cWc9PSIsInZhbHVlIjoieTlDQ3FuZDJWeUNwYmxtSE9DQWNcL1A2VE1VOG5iR2FxcEdpeFNkVHQ1Y0pEZWp4NzdQdkI2TStGKyt6UFY3UHFHUGtCRjVPbXVwamlIMUVOZitPMDRCRGRrbk9udWhxa1FxS1ZubFJlSEh4Y0J2clZubVhYRVRwMUI0K2Y3YTg2c3p4VVcxbklWZk1nbmZTeE9XM1dKTll1M3BtTk5wbHNnTEZFZWZOMW1NTURTOFRWMEk3ZU9yZkQzWnNCQnRcL2oiLCJtYWMiOiI1ZWM1NDZhZmQwMzJjY2YyYmRmMmVmMDRjNWIzYWQ5YTllNzA0NzllMjE3YTY5NGNkZGU1MWQ5YTFkNGE3ZTVlIn0%3D; XSRF-TOKEN=eyJpdiI6IkZvbUhNM3dxYmtPSlI3Z2Nxc2FTZEE9PSIsInZhbHVlIjoiY1YwbjVBbWRqZ0pUS3h2SnFuZUtIUWlJaHdZTnkyak4yVzQ1MzNFNEcwZmIzSEM0djN1aFFqOWtTQjB1Z2owTSIsIm1hYyI6ImQyMGRiMmUyMzQ3NzU2ZDE5ODgyOTFiMGNmZjNlM2Y1YWE5YTdkZDE1NmIxZTIxNmI1OTQzYjJkNDc3YjRjNDAifQ%3D%3D; wallhaven_session=eyJpdiI6IkQ4bCtYaFU0citnWFcwdzRUWGZJWVE9PSIsInZhbHVlIjoiK3BpVDZYMHpvYXNZa0puTkU1c28xOXZTSHEyMHpzcW9WdWd0OXJyRkhcLzVocEFrVk51ang2b1wvUThjbitOb29XIiwibWFjIjoiMDQ3NTFkNTk1YWU1ODM2OTNkZGI4Njk3OGVjMTk5MmExNWUxMjk0N2MxYTc2YThmZWNjNWUyOTVkYmQ5ODhmMCJ9'
    cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}

    # 图片保存文件夹
    # dir = f'download/{datetime.now().month}_{+datetime.now().day}/'

    dir = f'D:\学习\后端\Python\爬虫\code\Demo\wallhaven-download\download\chunmomo/'
    # 下载文件存放目录
    os.makedirs(dir, exist_ok=True)

    # 获取网页内容
    # resp = requests.get(url, headers={'User-Agent': ua.random})
    # soup = BeautifulSoup(resp.text, 'html.parser')

    # 获取图片URL列表
    img_urls = []

    count = 0

    with open('D:\学习\后端\Python\爬虫\code\Demo\wallhaven-download\\fail.txt') as f:
        lines = f.readlines()
        # 遍历图片地址
        for readline in lines:
            url = readline.rstrip()
            # 下载
            header = {'User-Agent': ua.random}
            # print(url)
            file_name = dir + url.split('/')[-1]

            # 请求地址
            r = requests.get(url, headers=header)
            content = r.content

            image_stream = BytesIO(content)

            try:
                # 尝试打开图片流
                Image.open(image_stream)
                with open(file_name, 'wb') as f:
                    f.write(content)
                count = count + 1
                print(f"{file_name} 下载完成")
            except Exception:
                print('失败' + url)
            finally:
                r.close()

    print("下载完成-", str(count))
