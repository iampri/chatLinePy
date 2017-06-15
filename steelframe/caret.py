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

class Caret():
    def time(self):
        ict = pytz.timezone('Asia/Bangkok')
        return timezone.now().astimezone(ict).strftime('%H:%M %p')
    
    def date(self):
        ict = pytz.timezone('Asia/Bangkok')
        return timezone.now().astimezone(ict).strftime('%A, %d %B %Y')
    
    def lottery(self):
        page = requests.get('http://lotto.mthai.com/tag/%E0%B8%AB%E0%B8%A7%E0%B8%A2%E0%B8%A3%E0%B8%B1%E0%B8%90%E0%B8%9A%E0%B8%B2%E0%B8%A5')
        tree = html.fromstring(page.content)
        period = tree.xpath('//p[@class="small-title show-for-small-only text-center hide-for-print"]/text()')[8:]
        prize1 = tree.xpath('//div[@id="prize-1"]/div/div/span/text()')
        prizel2 = tree.xpath('//div[@id="prize-l2"]/div/div/span/text()')
        prizef3 = tree.xpath('//div[@id="prize-f3"]/div/span/span/text()')
        prizel3 = tree.xpath('//div[@id="prize-l3"]/div/span/span/text()')
        prizen1 = tree.xpath('//div[@id="prize-n1"]/div/span/span/text()')
        return 'งวดวันที่ '+ period[0] + ", รางวัลที่ 1 " + prize1[0] + ', เลขท้าย 2 ตัว ' + prizel2[0] + ', เลขหน้า 3 ตัว ' + prizef3[0] + ', เลขท้าย 3 ตัว ' + prizel3[0] + ', รางวัลข้างเคียงรางวัลที่ 1 ' + prizen1[0]