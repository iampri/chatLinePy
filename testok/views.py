# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from steelframe.bot import BotChat

def index(request):
    botc = BotChat()
    platform = 'LINE'
    talker_id = 'Cd837b599d26fc150abe6133ab274fe95'
    reply_text = botc.reply_to(platform,talker_id,request.GET.get('m', 'money'))
    return HttpResponse(reply_text)