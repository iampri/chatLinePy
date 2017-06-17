# -*- coding: utf-8 -*-

# Copyright 2017 MYNASINGSWOO. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""
bot core
"""

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

WAITING_MINUTES = 5

BotName = ('M', 'อ', 'MONEY', 'MONEYPENNY', 'เอ็ม', 'เอ็มโมเน่', 'โมเน่', 'เอ็มโม', 'โม', 'เน่')
BotReply = ('ค่ะ', 'คะ', "yes ma'am", 'yes sir')

NotKnow = ['อยากไปเที่ยวจัง','เค้าเขินนะ..','^ ^','^ ^"','...','- -"','รัยอะ','เทอ เทอ มีแฟนยังอะ','ไปเที่ยวกันป่ะ','ช่วงนี้ดูอวบๆนะ','จะนอนยังอะ','- v -']

TrainCommand = ('จำนะ','สอน','เรียน','จำ','จำไว้','จำไว้นะ','ช่วยจำ','ช่วยจำนะ','จำไว้ที')
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
	""" bot chat """
	platform = ''
	talker_id = ''

	def __init__(self,platform,talker_id):
		platform = platform
		talker_id = talker_id

	def state(self):
		
		return ''

	def reply_to(self, message):
		reply_text = ''
		friend = Friend.objects.filter(user_id=self.talker_id, platform=self.platform).first()
		if friend:
			statec = StateChat.objects.filter(friend=friend).first()
			if statec:
				knownm = KnownMessage.objects.filter(say=message).values_list('reply', flat=True)
				if knownm:
					randoms = random.SystemRandom()
					reply_text = randoms.choice(knownm)



				else:
					unknownm = KnownMessage.objects.filter(say='2017dontknowword0617').values_list('reply', flat=True)
					randoms = random.SystemRandom()
					reply_text = randoms.choice(unknownm)

		return reply_text