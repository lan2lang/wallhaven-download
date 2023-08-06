import requests
from bs4 import BeautifulSoup
import os
import time
import imghdr


# 目标网页URLz
# categories(常规，动漫，人)，purity（健康，亚健康，黄），（1M，1d,1y）过去一个月
# url = 'https://wallhaven.cc/search?categories=111&purity=001&topRange=6M&sorting=toplist&order=desc&ai_art_filter=0'
url = 'https://wallhaven.cc/hot'

# 图片保存文件夹
dir = 'images-hot'

# 如果需要下载nsfw，需要添加cookie
cookie = ''
cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}
# print(cookie_dict)

# 获取网页内容
resp = requests.get(url,cookies=cookie_dict)
soup = BeautifulSoup(resp.text, 'html.parser')

# 获取图片URL列表
img_urls = []

imgType_list = {'jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif'}


# 在字符串指定位置插入字符
# str_origin：源字符串  pos：插入位置  str_add：待插入的字符串
#
def str_insert(str_origin, pos, str_add):
    str_list = list(str_origin)  # 字符串转list
    str_list.insert(pos, str_add)  # 在指定位置插入字符串
    str_out = ''.join(str_list)  # 空字符连接
    return str_out


for img in soup.find_all('img'):
    img_url = img.get('data-src')
    if img_url is not None:
        img_url = str(img_url).replace('th', 'w', 1).replace('small', 'full', 1)
        img_url = str_insert(img_url, img_url.rfind('/') + 1, 'wallhaven-')
        img_urls.append(str(img_url))

# 把找到的第一个th替换成w
# 把第一个small替换成full
# 在最后一个/后面加上wallhaven-
# jpg、png

# print(context)
# print(img_urls)
# print(len(img_urls))


# 保存图片到本地
if not os.path.exists(dir):
    # 创建 目录
    os.mkdir(dir)

# 记录请求开始时间
start = time.time()
print("开始时间：", start)

i = 0
for url in img_urls:
#     if i == 1:
#         break

    img_data = requests.get(url).content  # 从图片URL获取图片数据
    # print(img_urls[19])
    # img_data = requests.get(img_urls[19]).content  # 从图片URL获取图片数据

    fname = url.split('/')[-1]  # 从URL获取文件名

    file_url = os.path.join(dir, fname)
    # 将图片数据写入images文件夹
    with open(file_url, 'wb') as f:
        f.write(img_data)
    #
    if not imghdr.what(file_url) in imgType_list:

        # os.remove(file_url)  删除原文件

        # 重新下载

        file_url = file_url.removesuffix('jpg')
        file_url = file_url + 'png'

        # print(file_url)
        url = url.removesuffix('jpg')
        url = url + 'png'

        img_data = requests.get(url).content  # 从图片URL获取图片数据
        with open(file_url, 'wb') as f:
            f.write(img_data)

    i += 1

print('requests版爬虫耗时：', time.time() - start)
print('Done')
