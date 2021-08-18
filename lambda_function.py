import json
import os
import threading

import requests


class CircularBuffer:
    def __init__(self, array):
        self.max_size = len(array)
        self.pointer = 0
        self.buffer = array

    def get_three_items(self):
        three_items = [self.buffer[self.pointer], self.buffer[(self.pointer + 1) % self.max_size],
                       self.buffer[(self.pointer + 2) % self.max_size]]
        self.pointer = (self.pointer + 1) % self.max_size
        return three_items


def main():
    url = "https://api.airtable.com/v0/appDgJgMhHkLteXj9/MainTable?view=Grid%20view"
    key = "Bearer " + os.environ["API_KEY"]
    headers = {
        "Authorization": key
    }
    response = requests.get(url, headers=headers)
    records = json.loads(response.text)['records']

    titles = []
    for record in records:
        titles.append(record['fields']['title'])
    cb.buffer = titles
    cb.max_size = len(titles)
    return {
        'statusCode': 200,
        'body': json.dumps(" ".join(cb.get_three_items()), ensure_ascii=False).encode('utf8')
    }


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


cb = CircularBuffer([])


def lambda_handler(event, context):
    set_interval(main, 1)
