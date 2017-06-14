# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone
import dj_database_url

from steelframe.models import Friend, EventLog, StateChat, KnownMessage

WaitingMinutes = 5

class TestOKTestCase(TestCase):
    
    fixtures = ['steelframe.json']
    
    def test_cli(self):
        res = timezone.now() - timezone.timedelta(minutes=WaitingMinutes)
        self.assertNotEqual(res, timezone.now())
        #self.assertEqual(timezone.now(), res)
        f = Friend.objects.all().first()
        self.assertIsNotNone(f.modified_date)
        #self.assertEqual(f.modified_date, timezone.now())
        
        #idk why datetime in fixture will not load correctly, it will always be current date
        res2 = (f.modified_date > (timezone.now() - timezone.timedelta(minutes=WaitingMinutes)))
        self.assertFalse(res2)
        
        
        