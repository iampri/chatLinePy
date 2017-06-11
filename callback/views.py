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
import logging

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

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('django')


def index(request):
    #if request.path_info != '/callback/':
    #    return HttpResponseNotFound()

    # check request method
    #if request.method != 'POST':
    #    return HttpResponseNotAllowed(['POST'])

    # get X-Line-Signature header value
    #request_headers = {}
    #for header in request.META:
    #    if regex_http_x_line.match(header) or regex_content_length.match(header):
    #        request_headers[header] = request.META[header]

    if 'HTTP_X_LINE_SIGNATURE' in request.META:
        signature = request.META['HTTP_X_LINE_SIGNATURE']
    
    # get request body as text
    body = request.body.decode('utf-8')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return HttpResponseBadRequest()

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        if 'userId' in event['source']:
            logger.info("userId " + event.source.userId)
            
        if 'groupId' in event['source']:
            logger.info("groupId " + event.source.groupId)
            
        logger.info(event.message.text)
            
        if event.message.text.upper() == 'M':
            replyText = 'คะ'
        else:
            replyText = event.message.text
            
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=replyText)
        )
        
    return HttpResponse()

    