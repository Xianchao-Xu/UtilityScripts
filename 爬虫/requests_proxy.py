# coding: utf-8
# author: xuxc
import requests


def get_google():
    url = 'https://www.google.com'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/54.0.2840.99 "
                             "Safari/537.36"}
    proxy = '127.0.0.1:7890'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'http://' + proxy
    }
    response = requests.get(url, headers=headers, proxies=proxies)
    print(response.text)


if __name__ == '__main__':
    get_google()
