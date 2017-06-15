# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
import pytz

from lxml import html
import requests

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('django')

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, JoinEvent, MessageEvent, TextMessage, StickerMessage, TextSendMessage, 
)

class Ampersand():
    def stk(self,line_bot_api,token,parameters):
        if (parameters[0] == ';'): parameters = parameters[1:]
        pl = parameters.split(';')
        line_bot_api.reply_message(token,StickerMessage(sticker_id=pl[0],package_id=pl[1]))
        
    