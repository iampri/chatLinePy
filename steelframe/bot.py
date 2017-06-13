# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from steelframe.models import Friend, EventLog, StateChat

BotName = ('M','MONEY','MONEYPENNY','เอ็ม')
WaitingMinutes = 1

class BotChat():
    def reply_to(self, platform, talker_id, message):
        replyText = ''
        friend = Friend.objects.get(user_id=talker_id, platform=platform)
        if (friend):
            statec = StateChat.objects.get(friend_id=friend.id)
            if (statec):
                if (message.upper() in BotName):
                    statec.friend_id = friend
                    statec.state = StateChat.STATEWAIT
                    statec.modified_date = timezone.now
                    statec.save()
                    replyText = 'คะ'
                else:
                    if ((statec.state==StateChat.STATEWAIT) and (statec.modified_date > (timezone.now - timezone.timedelta(minutes=WaitingMinutes)))):
                        statec.modified_date = timezone.now
                        statec.save()

                        replyText = message

                    elif (statec.state!=StateChat.STATELEAVE):
                        statec.state = StateChat.STATELEAVE
                        statec.modified_date = timezone.now
                        statec.save()
                        
            else:
                statec = StateChat()
                statec.friend_id = friend
                statec.state = StateChat.STATELEAVE
                statec.modified_date = timezone.now
                statec.save()
                            
                    
                    
                    
                    



                    else:
                        statec = StateChat()
                        statec.friend_id = friend
                        statec.state = StateChat.STATELEAVE
                        statec.modified_date = timezone.now
                        statec.save()
                
                    
                    
                    
                    

                    

                    
        return replyText
    
    
    
    
    