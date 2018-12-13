# coding=utf-8
import re
import sys
import urllib
import requests



def get_onepage_urls(onepageurl):
    try:
        html = requests.get(onepageurl).text
    except Exception as e:
        print(e)
        pic_urls = []
        return pic_urls
    pdf_urls = re.findall('Lectures/.*?\.pdf', html)
    return pdf_urls


def down_pic(pic_urls, keyword, addurl):
    path = keyword + '\\'
    mkdir(path)
    for i, pic_url in enumerate(pic_urls):
        try:
            pic = requests.get(addurl + pic_url, timeout=5)
            string = path + pic_url.split('/')[1]
            with open(string, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s个文件: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s个文件时失败: %s' % (str(i + 1), str(pic_url)))
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
    addurl = "http://bwrcs.eecs.berkeley.edu/Classes/icdesign/ee241_s13/"
    url = "http://bwrcs.eecs.berkeley.edu/Classes/icdesign/ee241_s13/lectures.html"
    pdf_urls = get_onepage_urls(url)
    keyword = 'pdf'
    down_pdf(pdf_urls, keyword, addurl)
