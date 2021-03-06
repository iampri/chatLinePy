# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, JoinEvent, MessageEvent, TextMessage, StickerMessage, TextSendMessage, StickerSendMessage,
)

from steelframe.models import Friend, EventLog, StateChat, KnownMessage 
from steelframe.bot import BotChat

from callback.ampersand import Ampersand

import os
import sys
import logging
from random import randint

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Please specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Please specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
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

    # if event is MessageEvent and message is TextMessage
    for event in events:
        if isinstance(event, JoinEvent):
            talker_id = event.source.group_id
            logger.debug("join event, group_id: " + talker_id)
            profile = line_bot_api.get_profile(talker_id)
            friend = Friend()
            friend.platform = 'LINE'
            friend.user_id = talker_id
            friend.friend_type = 'GROUP'
            friend.display_name = profile.display_name
#            print(profile.picture_url)
#            print(profile.status_message)
            friend.save()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='แต้งกิ่ว'))
            logger.debug("insert: " + profile.display_name)
            continue
        if isinstance(event, FollowEvent):
            talker_id = event.source.user_id
            logger.debug("follow event, user_id: " + talker_id)
            profile = line_bot_api.get_profile(talker_id)
            friend = Friend()
            friend.platform = 'LINE'
            friend.user_id = talker_id
            friend.friend_type = 'PERSON'
            friend.display_name = profile.display_name
#            print(profile.picture_url)
#            print(profile.status_message)
            friend.save()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='แต้งกิ่ว'))
            logger.debug("insert: " + profile.display_name)
            continue
        if not isinstance(event, MessageEvent):
            continue
        
        if isinstance(event.message, StickerMessage):
            #logger.debug("sticker packageId: " + event.message.packageId + ", stickerId: " + event.message.stickerId)
            logger.debug("receive sticker message")
            
            #https://devdocs.line.me/files/sticker_list.pdf
            sId = randint(180, 259)
            #pId = randint(1, 3)
            line_bot_api.reply_message(event.reply_token,StickerSendMessage(sticker_id=sId,package_id=3))
        
        if not isinstance(event.message, TextMessage):
            continue

        if event.source.type == "user":
            talker_id = event.source.user_id
            logger.debug("user_id " + event.source.user_id)
            
        if event.source.type == "group":
            talker_id = event.source.group_id
            logger.debug("group_id " + event.source.group_id)
            
        talker_text = event.message.text    
        logger.debug(event.message.text)
        
        botc = BotChat()
        reply_message = botc.reply_to('LINE',talker_id,talker_text)
        if (reply_message):
            is_ampersandfunc = False
            if (reply_message[0] == '&'):
                ampersandMethods = [func for func in dir(Ampersand) if callable(getattr(Ampersand, func)) and not func.startswith("__")]
                ampersand = Ampersand()
                for method in ampersandMethods:
                    pos = reply_message.find(method) 
                    if (pos == 1):
                        is_ampersandfunc = True
                        mtd = getattr(ampersand, method)
                        
                        parameters = reply_message[len(method)+1:]
                        res = mtd(line_bot_api,event.reply_token,parameters)
                        
                        break
            
            if (not is_ampersandfunc):                            
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_message))
        

        
    #group_id = "Cd837b599d26fc150abe6133ab274fe95"
    #line_bot_api.push_message(group_id, TextSendMessage(text='ก็ได้นะ'))
    
    return HttpResponse()

    