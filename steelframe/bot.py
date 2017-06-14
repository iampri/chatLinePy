# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from steelframe.models import Friend, EventLog, StateChat, KnownMessage
from steelframe.caret import Caret

import random
import re

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('django')

WaitingMinutes = 5
BotName = ('M','อ','MONEY','MONEYPENNY','เอ็ม','เอ็มโมเน่','โมเน่','เอ็มโม','โม','เน่')
BotReply = ('ค่ะ','คะ',"yes ma'am",'yes sir')

NotKnow = ['อยากไปเที่ยวจัง','เค้าเขินนะ..','^ ^','^ ^"','...','- -"','รัยอะ','พูดภาษาคนดิ','เทอ เทอ มีแฟนยังอะ','ไปเที่ยวกันป่ะ','ช่วงนี้ดูอวบๆนะ','จะนอนยังอะ','- v -']

TrainCommand = ('จำนะ','สอน','เรียน','จำ','จำไว้','จำไว้นะ')
TrainCommandReply = ['เย้!!','จำจำจำ เย้..']
TrainSayWord = ('พูดว่า','พูด','ถ้าพูดว่า')
TrainReplyWord = ('ตอบว่า','ตอบ','ให้ตอบว่า')
TrainEndWord = ('จบ','พอละ','แค่นี้')

RepeatForReply = 'ให้ตอบว่างัยคะ'
RepeatSay = 'พูดว่า'
RepeatReply = 'ให้ตอบว่า'

Yes = ['ค่ะ','ได้ค่ะ','ดั้ยค่ะ','ได้เลย','ก็ได้']

Thankyou = ['ขอบคุณคะ','จัยจร้า','หว้าา..า']

BotStop = ('หยุด','เงียบ','stop','shutup', 'shut up')

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
                    randoms = random.SystemRandom()
                    replyText = randoms.choice(BotReply)
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
                            randoms = random.SystemRandom()
                            replyText = randoms.choice(TrainCommandReply)
                            logger.debug("call train")
                        else:
                            knownm = KnownMessage.objects.filter(say=message).values_list('reply', flat=True)
                            if (knownm):
                                randoms = random.SystemRandom()
                                replyText = randoms.choice(knownm)
                                if (replyText.find("^") != -1):
                                    caretMethods = [func for func in dir(Caret) if callable(getattr(Caret, func)) and not func.startswith("__")]
                                    caret = Caret()
                                    for method in caretMethods:
                                        if (replyText.find(method) > 0):
                                            mtd = getattr(caret, method)
                                            res = mtd()
                                            replyText = replyText.replace('^'+method,res)
                                        
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
                            knownm = KnownMessage.objects.filter(reply=None,friend=friend).first()
                            if (not knownm):
                                knownm = KnownMessage()
                            knownm.friend = friend
                            knownm.say = message.replace(sw.group(1), ' ', 1).strip()
                            knownm.reply = None
                            knownm.save()
                            replyText = message + " " + RepeatForReply
                            
                        rw = re.search(r"(^("+'|'.join(TrainReplyWord)+r"))",message)
                        if rw:
                            logger.debug("found rw: " + rw.group(1))
                            knownm = KnownMessage.objects.filter(reply=None,friend=friend).first()
                            knownm.reply = message.replace(rw.group(1), ' ', 1).strip()
                            knownm.save()
                            replyText = RepeatSay + knownm.say + ' ' + RepeatReply + knownm.reply
                            
                        if (message.upper() in TrainEndWord):
                            statec.state = StateChat.STATEWAIT
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
    
    
    
    
    