# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Friend(models.Model):
    display_name = models.CharField(max_length=200)
    friend_type = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return 'platform: ' + self.platform + ', friend_type: ' + self.friend_type + ', display_name: ' + self.display_name

class EventLog(models.Model):
    friend = models.ForeignKey(Friend)
    event_name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.event_name

class StateChat(models.Model):
    """
    StateChat is for keeping current chat state
    """
    STATEWAIT = 'WAIT'
    STATELEAVE = 'LEAVE'
    STATETRAIN = 'TRAIN'

    friend = models.ForeignKey(Friend)
    state = models.CharField(max_length=100, default='LEAVE')
    modified_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return 'friend: ' + self.friend.display_name + ' state: ' + self.state

class KnownMessage(models.Model):
    """a"""
    friend = models.ForeignKey(Friend)
    say = models.CharField(max_length=200)
    reply = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        #r = ' ' if self.reply is None else self.reply
        return 'friend: ' + self.friend.display_name + ' say: ' + self.say + ' reply: ' + self.reply
