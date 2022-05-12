from pymongo import MongoClient
from flask import Flask, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.cracker

app.config["TEMPLATES_AUTO_RELOAD"] = True

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://search.naver.com/search.naver?where=view&sm=tab_jum&query=%EB%A7%9B%EC%A7%91',
                    headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

SECRET_KEY = 'Cracker'

bp = Blueprint('blog', __name__)

##Left column of Blog links##
@bp.route('/blog', methods=["GET"])
def get_blog():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(
        'https://search.naver.com/search.naver?sm=tab_hty.top&where=view&query=%EC%84%9C%EC%9A%B8+%EB%A7%9B%EC%A7%91&oquery=%EB%A7%9B%EC%A7%91&tqi=hFpCvsprvh8ssAWQZGwssssss7G-351156&mode=normal',
        headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    trs = soup.select(
        '#main_pack > section > div > div._list > panel-list > div:nth-child(1) > more-contents > div > ul > li')[0:5]
    blog_list = []

    for tr in trs:
        a_tag = tr.select_one('div.total_wrap.api_ani_send > div > a')
        if a_tag is not None:
            title = a_tag.text
            link = a_tag.get("href")

            doc = {
                'title': title,
                'link': link
            }
            blog_list.append(doc)

    return jsonify({'result': 'success', 'blog_list': blog_list})

##Middle column of Blog links##
@bp.route('/blogmiddle', methods=["GET"])
def get_blog_middle():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(
        'https://search.naver.com/search.naver?sm=tab_hty.top&where=view&query=%EC%84%9C%EC%9A%B8+%EB%A7%9B%EC%A7%91&oquery=%EB%A7%9B%EC%A7%91&tqi=hFpCvsprvh8ssAWQZGwssssss7G-351156&mode=normal',
        headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    trs = soup.select(
        '#main_pack > section > div > div._list > panel-list > div:nth-child(1) > more-contents > div > ul > li')[6:11]

    blog_list_middle = []

    for tr in trs:
        a_tag = tr.select_one('div.total_wrap.api_ani_send > div > a')
        if a_tag is not None:
            title = a_tag.text[0:35]
            link = a_tag.get("href")

            docmiddle = {
                'title': title,
                'link': link
            }
            blog_list_middle.append(docmiddle)
    return jsonify({'result': 'success', 'blog_list_middle': blog_list_middle})
