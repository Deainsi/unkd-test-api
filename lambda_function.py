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


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello World')
    }
