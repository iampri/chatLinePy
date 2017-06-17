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
test case
"""


from __future__ import unicode_literals
# pylint: disable=E0401
from django.test import TestCase
from .bot import BotChat

class Bot(TestCase):
    """Bot test case"""
    def test_init(self):
        """test_init"""
        bot_chat = BotChat('LINE', 'Cd837b599d26fc150abe6133ab274fe95')
        self.assertIsNotNone(bot_chat)

    def test_reply_to_empty_string(self):
        """ test_reply_to """
        bot_chat = BotChat('LINE', 'Cd837b599d26fc150abe6133ab274fe95')
        res = bot_chat.reply_to('testing')
        self.assertFalse(res)

    def test_reply_to_have_string(self):
        """ test_reply_to with return value"""
        bot_chat = BotChat('LINE', 'Cd837b599d26fc150abe6133ab274fe95')
        res = bot_chat.reply_to('2017dontknowword0617')
        self.assertIsNone(res)
