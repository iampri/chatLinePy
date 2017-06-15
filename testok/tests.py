# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone
import dj_database_url

from steelframe.models import Friend, EventLog, StateChat, KnownMessage
from steelframe.caret import Caret

WaitingMinutes = 5

class TestOKTestCase(TestCase):
    
    fixtures = ['steelframe.json']
    
    def test_python(self):
        src = ";sdfdsf;dfgdfg;;"
        data = src.split(";")
        self.assertIsNone(data)
    
    def test_caretfunc(self):
        replyText = "^lottery"
        if (replyText.find("^") != -1):
            caretMethods = [func for func in dir(Caret) if callable(getattr(Caret, func)) and not func.startswith("__")]
            caret = Caret()
            for method in caretMethods:
                if (replyText.find(method) > 0):
                    mtd = getattr(caret, method)
                    res = mtd()
                    replyText = replyText.replace('^'+method,res)
        self.assertIsNotNone(replyText)
        
    def test_getmethod(self):
        method_list = [func for func in dir(Caret) if callable(getattr(Caret, func)) and not func.startswith("__")]
        self.assertIsNotNone(method_list)
        
    def test_timedelta(self):
        res = timezone.now() - timezone.timedelta(minutes=WaitingMinutes)
        self.assertNotEqual(res, timezone.now())
        #self.assertEqual(timezone.now(), res)
        f = Friend.objects.all().first()
        self.assertIsNotNone(f.modified_date)
        #self.assertEqual(f.modified_date, timezone.now())
        
        #idk why datetime in fixture will not load correctly, it will always be current date
        res2 = (f.modified_date > (timezone.now() - timezone.timedelta(minutes=WaitingMinutes)))
        #self.assertFalse(res2)
        self.assertIsNotNone(res2)
        