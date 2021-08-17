import json
import os
import time

import requests


class CircularBuffer:
    def __init__(self, array):
        self.max_size = len(array)
        self.pointer = 0
        self.buffer = array

    def get_three_items(self):
        while True:
            yield [self.buffer[self.pointer], self.buffer[(self.pointer + 1) % self.max_size],
                   self.buffer[(self.pointer + 2) % self.max_size]]
            time.sleep(3)
            self.pointer = (self.pointer + 1) % self.max_size


def lambda_handler():
    url = "https://api.airtable.com/v0/appDgJgMhHkLteXj9/MainTable?view=Grid%20view"
    key = "Bearer " + "keylqsbeqJwvC6hst"
    headers = {
        "Authorization": key
    }
    response = requests.get(url, headers=headers)
    records = json.loads(response.text)['records']

    titles = []
    for record in records:
        titles.append(record['fields']['title'])

    cb = CircularBuffer(titles)
    # for i in cb.get_three_items():
    #     return {
    #         'statusCode': 200,
    #         'body': json.dumps(" ".join(i))
    #     }
    return {
        'statusCode': 200,
        'body': json.dumps(key)}
