from __future__ import print_function
import time
import json
import os
import requests
import lxml.html
from definition_of_tonality import analysis
from lxml.cssselect import CSSSelector

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)'
url_youtube_video = 'https://www.youtube.com/all_comments?v={youtube_id}'
YOUTUBE_COMMENTS_AJAX_URL = 'https://www.youtube.com/comment_ajax'


def delete_file(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        pass


def find_value(html, key, num_chars=2):
    pos_begin = html.find(key) + len(key) + num_chars
    pos_end = html.find('"', pos_begin)
    return html[pos_begin: pos_end]


def extract_comments(html):
    tree = lxml.html.fromstring(html)
    item_sel = CSSSelector('.comment-item')
    text_sel = CSSSelector('.comment-text-content')

    for item in item_sel(tree):
        yield {'cid': item.get('data-cid'),
               'text': text_sel(item)[0].text_content()}


def extract_reply_cids(html):
    tree = lxml.html.fromstring(html)
    sel = CSSSelector('.comment-replies-header > .load-comments')
    return [i.get('data-cid') for i in sel(tree)]


def ajax_request(session, url, params, data, retries=10, sleep=20):
    for _ in range(retries):
        response = session.post(url, params=params, data=data)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            return response_dict.get('page_token', None), response_dict['html_content']
        else:
            time.sleep(sleep)


def download_comments(youtube_id, sleep=1):
    session = requests.Session()
    session.headers['User-Agent'] = user_agent

    response = session.get(url_youtube_video.format(youtube_id=youtube_id))
    html = response.text
    reply_cids = extract_reply_cids(html)

    ret_cids = []
    for comment in extract_comments(html):
        ret_cids.append(comment['cid'])
        yield comment

    page_token = find_value(html, 'data-token')
    session_token = find_value(html, 'XSRF_TOKEN', 4)

    first_iteration = True

    while page_token:
        data = {'video_id': youtube_id,
                'session_token': session_token}

        params = {'action_load_comments': 1,
                  'order_by_time': True,
                  'filter': youtube_id}

        if first_iteration:
            params['order_menu'] = True
        else:
            data['page_token'] = page_token

        response = ajax_request(session, YOUTUBE_COMMENTS_AJAX_URL, params, data)
        if not response:
            break

        page_token, html = response

        reply_cids += extract_reply_cids(html)
        for comment in extract_comments(html):
            if comment['cid'] not in ret_cids:
                ret_cids.append(comment['cid'])
                yield comment

        first_iteration = False
        time.sleep(sleep)

    for cid in reply_cids:
        data = {'comment_id': cid,
                'video_id': youtube_id,
                'can_reply': 1,
                'session_token': session_token}

        params = {'action_load_replies': 1,
                  'order_by_time': True,
                  'filter': youtube_id,
                  'tab': 'inbox'}

        response = ajax_request(session, YOUTUBE_COMMENTS_AJAX_URL, params, data)
        if not response:
            break

        _, html = response

        for comment in extract_comments(html):
            if comment['cid'] not in ret_cids:
                ret_cids.append(comment['cid'])
                yield comment
        time.sleep(sleep)


def result_analysis():
    files = ['negative.txt', 'neutral.txt', 'positive.txt', 'skip.txt', 'speech.txt']
    for file in files:
        delete_file(file)
    youtube_id = input('Введите id видео:')
    print('Обработка комментариев...')
    count = 0
    positive = 0
    neutral = 0
    negative = 0
    skip = 0
    speech_act_class = 0
    for comment in download_comments(youtube_id):
        tonality = analysis(comment['text'])
        if tonality == "skip":
            skip += 1
            skip_file = open('skip.txt', 'a')
            skip_file.write(comment['text'] + '\n')
            skip_file.write('----------------------' + '\n')

        if tonality == "negative":
            negative += 1
            negative_file = open('negative.txt', 'a')
            negative_file.write(comment['text'] + '\n')
            negative_file.write('----------------------' + '\n')

        if tonality == "neutral":
            neutral += 1
            neutral_file = open('neutral.txt', 'a')
            neutral_file.write(comment['text'] + '\n')
            neutral_file.write('----------------------' + '\n')

        if tonality == "positive":
            positive += 1
            positive_file = open('positive.txt', 'a')
            positive_file.write(comment['text'] + '\n')
            positive_file.write('----------------------' + '\n')

        if tonality == "speech":
            speech_act_class += 1
            speech_file = open('speech.txt', 'a')
            speech_file.write(comment['text'] + '\n')
            speech_file.write('----------------------' + '\n')

    count += 1

    return skip, negative, positive, neutral, speech_act_class
