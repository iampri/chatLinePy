# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
import pytz

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
    
    