import os
import ssl
from time import sleep

import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib3 import PoolManager
from requests.adapters import HTTPAdapter
import secrets
import string
import time
import requests
from requests.adapters import HTTPAdapter, Retry

# 创建带重试的 session
session = requests.Session()
retries = Retry(
    total=5,                # 重试次数
    backoff_factor=1,       # 1s, 2s, 4s 递增等待
    status_forcelist=[500, 502, 503, 504, 429],
)

session.mount("https://", HTTPAdapter(max_retries=retries))
session.mount("http://", HTTPAdapter(max_retries=retries))

def download_image(url, save_path):
    for attempt in range(5):  # 自带额外兜底重试
        try:
            with session.get(url, cookies=cookies, headers=headers, stream=True, timeout=20) as r:
                r.raise_for_status()
                
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 64):  # 64 KB 块
                        if chunk:
                            f.write(chunk)

            print(f"下载成功: {save_path}")
            return True

        except Exception as e:
            print(f"下载失败（尝试 {attempt+1}/5）：{e}")
            time.sleep(2)

    print(f"最终失败: {url}")
    return False


def gen_seed(length=6):
    chars = string.ascii_letters  # 大写 + 小写
    return ''.join(secrets.choice(chars) for _ in range(length))

# 示例

# 代理设置（可选）
# proxies = {
#     'http': 'http://127.0.0.1:7897',
#     'https': 'https://127.0.0.1:7897',
# }

# class TLSAdapter(HTTPAdapter):
#     def init_poolmanager(self, *args, **kwargs):
#         ctx = ssl.create_default_context()
#         ctx.set_ciphers("DEFAULT:@SECLEVEL=1")  # 降低安全等级
#         kwargs["ssl_context"] = ctx
#         return super().init_poolmanager(*args, **kwargs)

# session = requests.Session()
# session.mount("https://", TLSAdapter())

# 请求头设置，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 设置 Cookie（在浏览器的开发者工具中获取）
cookies = {
    'wallhaven_session': 'eyJpdiI6IkhxcFo3M0liQzRwMWhHTzNGUEc0RXc9PSIsInZhbHVlIjoiQkxiWHcrSE12dVo2ZThSWmlqbVwvUVg4b0p3VXUzXC9sallDXC9JVE5kY0YzWEh4Q1NJVnhuZ0xjZkxIU3grMmRNdSIsIm1hYyI6ImVlZDgyYmM2N2UxYTgxMTA4OTYyYTMxODRlNWNhYmVmMDFjMzRkZTk4ZWVlNTQ3NjA0NmNhYTJlOWZjY2Q5ZmIifQ%3D%3D'
}

# 保存图片的文件夹路径
save_dir = "C:\\Users\\zou23\\Pictures\\桜桃喵"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 爬取的页数范围
start_num=20
total_pages = 25  # 总共有22页
aspect_ratio_tolerance=4
# 遍历所有页数
for page_num in range(start_num, total_pages + 1):
    # 构建当前页的URL
    seed=gen_seed()
    url=f'https://wallhaven.cc/search?q=%E6%A1%9C%E6%A1%83%E5%96%B5&categories=111&purity=111&sorting=views&order=desc&page={page_num}'
    # url = f"https://wallhaven.cc/search?q=id%3A12757&categories=111&atleast=1920x1080&purity=011&sorting=random&order=desc&seed={seed}&page={page_num}"
    # url='https://wallhaven.cc/search?q=id%3A12757&categories=111&purity=111&sorting=date_added&order=desc&page=1'
    print(url)
    
    # 
    # 原神R18 https://wallhaven.cc/search?q=id%3A95047&categories=001&purity=001&sorting=views&order=desc&page=1
    # 随机cosplayR https://wallhaven.cc/search?q=id%3A12757&categories=111&purity=011&sorting=random&order=desc&seed=gen_seed()&page=1
    # 碧蓝航线 id%3A67333
    # 获取网页内容
    response = requests.get(url, cookies=cookies,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有缩略图的链接
    img_tags = soup.find_all("a", class_="preview")

    # 遍历每个缩略图链接
    for img_tag in img_tags:
        # 获取原图页面的URL
        img_page_url = img_tag["href"]
        
        # 获取原图页面的内容
        img_page_response = requests.get(img_page_url, cookies=cookies,headers=headers)
        img_page_soup = BeautifulSoup(img_page_response.text, 'html.parser')

       # 查找图片链接
        img_tag = img_page_soup.find("img", id="wallpaper")

        if img_tag:
            # 使用 get() 方法避免 KeyError
            original_img_url = img_tag.get("src")
            
            if original_img_url:
                print(f"找到原图链接: {original_img_url}")

                # 获取图片的名称和保存路径
                img_name = os.path.join(save_dir, original_img_url.split("/")[-1])

                download_image(original_img_url, img_name)

                # 下载原图
#                 img_data = requests.get(original_img_url, cookies=cookies,headers=headers).content

# # 使用 Pillow 加载图片并检查其尺寸
#                 # image = Image.open(BytesIO(img_data))
#                 # width, height = image.size
#   # 计算宽高比
#                 # aspect_ratio = width / height
#                 # 如果图片的宽度或高度小于 2560x1440，跳过该图片
#                 # if width < 2560 or height < 1440 or width < height:
#                 #     print(f"图片 {img_name} 的分辨率 ({width}x{height}) 小于 2K或者不是横图，跳过...")
#                 #     continue
                
#                 # # 判断9:16比例，宽高比接近0.5625
#                 # if not (abs(aspect_ratio - 16/9) <= aspect_ratio_tolerance):
#                 #     print(f"图片 {img_name} 被跳过: 不是9:16比例，宽高比: {aspect_ratio:.4f}")
#                 #     continue
#                 # 保存图片
#                 with open(img_name, 'wb') as f:
#                     f.write(img_data)

                # print(f"下载完成: {img_name}")
            else:
                print(f"没有找到原图链接: {img_page_url}")
    
    print(f"第 {page_num} 页下载完成!")
    sleep(1)

print("所有原图下载完成!")
