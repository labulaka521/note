#  队列
import requests


def count_word_url(url):
    resp = requests.get(url)
    return len(resp.text.split())


