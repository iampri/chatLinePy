# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone
from steelframe.models import Friend, EventLog, StateChat, KnownMessage

WaitingMinutes = 5

class TestOKTestCase(TestCase):
    def setup(self):
        pass
    
    def test_cli(self):
        res = timezone.now() + timezone.timedelta(minutes=WaitingMinutes)
        self.assertNotEqual(res, timezone.now())
        #self.assertEqual(res, timezone.now())
        #statec = StateChat.objects.all()[:1].get()
        statec = Friend.objects.all().first()
        self.assertIsNotNone(statec)
        res2 = (statec.modified_date > (timezone.now() + timezone.timedelta(minutes=WaitingMinutes)))
        self.assertFalse(res2)
        
        
        