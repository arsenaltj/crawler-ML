# coding=utf-8
"""根据搜索词下载百度图片"""
import re
import sys
import urllib

import requests


def getPage(keyword, page, n):
    page = page * n
    keyword = urllib.parse.quote(keyword, safe='/')
    google_url = 'https://www.google.com.hk/search?q=' + \
        keyword + '&safe=strict&source=lnms&tbm=isch'
    url_begin = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="
    url = url_begin + keyword + "&pn=" + \
        str(page) + "&gsm=" + str(hex(page)) + \
        "&ct=&ic=0&lm=-1&width=0&height=0"
    print(google_url)
    return google_url


def get_onepage_urls(onepageurl):
    try:
        html = requests.get(onepageurl).text
        #print(html)
    except Exception as e:
        print(e)
        pic_urls = []
        return pic_urls
    google_pic_urls = re.findall('src="(.*?)",', html, re.S)
    print(google_pic_urls)
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    return google_pic_urls


def down_pic(pic_urls,keyword):
    """给出图片链接列表, 下载所有图片"""
    path = keyword + '\\'
    mkdir(path)
    for i, pic_url in enumerate(pic_urls):
        try:
            pic = requests.get(pic_url, timeout=5)
            string = path + str(i + 1) + '.jpg'
            with open(string, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path+' 创建成功')
        return True
    else:
        print(path+' 目录已存在')
        return False


if __name__ == '__main__':
    keyword = '狗'  # 关键词, 改为你想输入的词即可, 相当于在百度图片里搜索一样
    page_begin = 0
    page_number = 30
    image_number = 2
    all_pic_urls = []
    while 1:
        if page_begin > image_number:
            break
        print("第%d次请求数据", page_begin)
        url = getPage(keyword, page_begin, page_number)
        onepage_urls = get_onepage_urls(url)
        page_begin += 1

        all_pic_urls.extend(onepage_urls)
    print (len(list(set(all_pic_urls))))
    down_pic(list(set(all_pic_urls)),keyword)
