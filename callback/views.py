# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import sys
import re

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

regex_http_x_line = re.compile(r'^HTTP_X_LINE_SIGNATURE$')
regex_content_length = re.compile(r'^CONTENT_LENGTH$')

def index(request):
    #if request.path_info != '/callback/':
    #    return HttpResponseNotFound()

    # check request method
    #if request.method != 'POST':
    #    return HttpResponseNotAllowed(['POST'])

    # get X-Line-Signature header value
    request_headers = {}
    for header in request.META:
        if regex_http_x_line.match(header) or regex_content_length.match(header):
            request_headers[header] = request.META[header]

    # get request body as text
    body = request.body.decode('utf-8')

    # parse webhook body
    try:
        events = parser.parse(body, request_headers['HTTP_X_LINE_SIGNATURE'])
    except InvalidSignatureError:
        return HttpResponseBadRequest()

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    return HttpResponse()

    