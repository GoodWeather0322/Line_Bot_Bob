# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import requests
import re
import random
import configparser
import urllib.request
from argparse import ArgumentParser
from bs4 import BeautifulSoup

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if event.message.text == "Hibob":
        buttons_template = TemplateSendMessage(
            alt_text='Bob說你好',
            template=ButtonsTemplate(
                title='BOB的功能',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='BOB現在很廢 沒有功能',
                        text='BOB現在很廢 沒有功能'
                    ),
                    MessageTemplateAction(
                        label='BOB現在很廢 只會回話',
                        text='BOB現在很廢 只會回話'
                    ),
                    MessageTemplateAction(
                        label='天氣',
                        text='天氣'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    elif event.message.text == "天氣":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="想知道嗎，自己查\nhttps://www.cwb.gov.tw/V7/index.htm")
        return 0
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        return 0
    )

    #print(event) {"message": {"id": "7383075542344", "text": "T", "type": "text"}, "replyToken": "bb86d70489324c9d97a4e3e62b581fe6", "source": {"type": "user", "userId": "Uec77d4b728f94e4f02c6aac6b15e5788"}, "timestamp": 1517130847372, "type": "message"}
    #print(TextMessage) <class 'linebot.models.messages.TextMessage'>
    #print(MessageEvent) <class 'linebot.models.events.MessageEvent'>


@handler.add(MessageEvent, message=ImageMessage)
def message_image(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="this is an image")
    )
    #print(event) {"message": {"id": "7383080355073", "type": "image"}, "replyToken": "c6085bb46d0247f1928a650398316177", "source": {"type": "user", "userId": "Uec77d4b728f94e4f02c6aac6b15e5788"}, "timestamp": 1517130917849, "type": "message"}
    #print(ImageMessage) <class 'linebot.models.messages.ImageMessage'>
    #print(MessageEvent) <class 'linebot.models.events.MessageEvent'>

@handler.add(MessageEvent, message=VideoMessage)
def message_video(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="this is an video")
    )

@handler.add(MessageEvent, message=AudioMessage)
def message_audio(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="this is an audio")
    )

@handler.add(MessageEvent, message=LocationMessage)
def message_location(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="this is an location")
    )

@handler.add(MessageEvent, message=StickerMessage)
def message_sticker(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="this is an sticker")
    )
    print(event)

@handler.add(MessageEvent, message=FileMessage)
def message_file(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="this is an file")
    )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)