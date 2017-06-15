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

class Jobs():
    def run(self):
        
        logger.debug("job run")

    