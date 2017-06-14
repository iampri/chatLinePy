# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from steelframe.models import Friend, EventLog, StateChat, KnownMessage

import random
import re

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('django')

WaitingMinutes = 5
BotName = ('M','MONEY','MONEYPENNY','เอ็ม')
TrainCommand = ('จำนะ','สอน','เรียน','จำ','จำไว้','จำไว้นะ')
NotKnow = ['อยากไปเที่ยวจัง','เรารู้จักกันเหรอ','เค้าเขินนะ..','^ ^','^ ^"','...','- -"','รัยอะ']
TrainSayWord = ('พูดว่า','พูด','ถ้าพูดว่า')
TrainReplyWord = ('ตอบว่า','ตอบ','ให้ตอบว่า')
TrainEndWord = ('จบ','พอละ','แค่นี้')

RepeatForReply = 'ให้ตอบว่างัยคะ'
RepeatSay = 'พูดว่า'
RepeatReply = 'ให้ตอบว่า'

Yes = ['คะ','ได้คะ','ดั้ยคะ','ได้เลย','ก็ได้']

Thankyou = ['ขอบคุณคะ','จัยจร้า','จุบุจุบุ']

BotStop = ('หยุด','เงียบ','stop')

#need optimize!!
class BotChat():
    def reply_to(self, platform, talker_id, message):
        replyText = ''
        friend = Friend.objects.filter(user_id=talker_id, platform=platform).first()
        if (friend):
            statec = StateChat.objects.filter(friend=friend).first()
            if (statec):
                if (message.upper() in BotName):
                    statec.friend = friend
                    statec.state = StateChat.STATEWAIT
                    statec.modified_date = timezone.now()
                    statec.save()
                    #randoms = random.SystemRandom()
                    #replyText = randoms.choice(Yes)
                    replyText = 'คะ'
                    logger.debug("call m")
                elif (message.upper() in BotStop):
                    statec.state = StateChat.STATELEAVE
                    statec.modified_date = timezone.now()
                    statec.save()
                    randoms = random.SystemRandom()
                    replyText = randoms.choice(Yes)
                    logger.debug("order stop")
                else:
                    if ((statec.state==StateChat.STATEWAIT) and (statec.modified_date > (timezone.now() - timezone.timedelta(minutes=WaitingMinutes)))):
                        if (message.upper() in TrainCommand):
                            statec.state = StateChat.STATETRAIN
                            replyText = 'เย้!!'
                            logger.debug("call train")
                        else:
                            knownm = KnownMessage.objects.filter(say=message).first()
                            if (knownm):
                                replyText = knownm.reply
                                logger.debug("found " + message + " in db and reply: " + replyText)
                            else:
                                randoms = random.SystemRandom()
                                replyText = randoms.choice(NotKnow)
                                logger.debug("Not found " + message + " in db and reply: " + replyText)
                                
                        statec.modified_date = timezone.now()
                        statec.save()
                    elif ((statec.state==StateChat.STATETRAIN) and (statec.modified_date > (timezone.now() - timezone.timedelta(minutes=WaitingMinutes)))):
                        
                        sw = re.search(r"(^("+'|'.join(TrainSayWord)+r"))",message)
                        if sw:
                            logger.debug("found sw: " + sw.group(1))
                            knownm = KnownMessage()
                            knownm.friend = friend
                            knownm.say = message.replace(sw.group(1), ' ', 1).strip()
                            knownm.reply = None
                            knownm.save()
                            replyText = message + " " + RepeatForReply
                            
                        rw = re.search(r"(^("+'|'.join(TrainReplyWord)+r"))",message)
                        if rw:
                            logger.debug("found rw: " + rw.group(1))
                            knownm = KnownMessage.objects.filter(reply=None).first()
                            knownm.reply = message.replace(rw.group(1), ' ', 1).strip()
                            knownm.save()
                            replyText = RepeatSay + knownm.say + ' ' + RepeatReply + knownm.reply
                            
                        if (message.upper() in TrainEndWord):
                            statec.state==StateChat.STATEWAIT
                            randoms = random.SystemRandom()
                            replyText = randoms.choice(Thankyou)
                            
                        statec.modified_date = timezone.now()
                        statec.save()
                    elif (statec.state!=StateChat.STATELEAVE):
                        statec.state = StateChat.STATELEAVE
                        statec.modified_date = timezone.now()
                        statec.save()
            # if (statec):         
            else:
                statec = StateChat()
                statec.friend = friend
                statec.state = StateChat.STATELEAVE
                statec.modified_date = timezone.now()
                statec.save()
                            
                    
        return replyText
    
    
    
    
    