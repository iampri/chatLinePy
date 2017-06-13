# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Friend,EventLog,StateChat

admin.site.register(Friend)

admin.site.register(EventLog)

admin.site.register(StateChat)
