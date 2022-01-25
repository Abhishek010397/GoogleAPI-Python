from json import dumps
from httplib2 import Http
import argparse

def post_message(message):
    url = 'https://chat.googleapis.com/v1/spaces/messages'
    bot_message = {
        'text' : message
    }

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print(response)


