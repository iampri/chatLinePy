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

"""for general testing"""

from __future__ import unicode_literals

import sys

# pylint: disable=E0401
from django.test import TestCase
# pylint: disable=unused-import
from django.utils import timezone
import dj_database_url

from steelframe.models import Friend, EventLog, StateChat, KnownMessage
from steelframe.caret import Caret
from job.jobs import Jobs

WAIT_MINUTES = 5

class TestOKTestCase(TestCase):
    """un-specific test case"""
    fixtures = ['steelframe.json']

    def test_q_d(self):
        """quick and dirty test"""
        dec = sys.getdefaultencoding()
        #self.failUnless(not dec)
        self.assertNotEqual(dec, 'x')

    def test_encoding(self):
        """test_encoding"""
        dec = sys.getdefaultencoding()
        #self.failUnless(not dec)
        self.assertNotEqual(dec, 'encoding')

    def test_caretfunc(self):
        """ caret func """
        reply_text = "^lottery"
        if reply_text.find("^") != -1:
            # pylint: disable=C0301
            caret_methods = [func for func in dir(Caret) if callable(getattr(Caret, func)) and not func.startswith("__")]
            caret = Caret()
            for method in caret_methods:
                if reply_text.find(method) > 0:
                    mtd = getattr(caret, method)
                    res = mtd()
                    reply_text = reply_text.replace('^'+method, res)
        self.assertIsNotNone(reply_text)
        