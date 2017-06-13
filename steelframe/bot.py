# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from steelframe.models import Friend, EventLog, StateChat

BotName = ('M','MONEY','MONEYPENNY','เอ็ม')

class BotChat():
    def reply_to(self, platform, talker_id, message):
        replyText = ''
        friend = Friend.objects.get(user_id=talker_id, platform=platform)
        if (message.upper() in BotName):
            if(friend):
                statec = StateChat()
                statec.friend_id = friend.id
                statec.state = StateChat.STATEWAIT
            replyText = 'คะ'
        else:
            if(friend):
                statec = StateChat.objects.get(friend_id=friend.id)
                if(not statec):
                    statec.friend_id = friend.id
                    statec.state = StateChat.STATELEAVE
                    statec.save()
                
                if(statec.state==StateChat.STATEWAIT):
                    replyText = message
                else:
                    replyText = ''
                    
        return replyText
    
    
    
    
    