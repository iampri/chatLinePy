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
        
    def follow(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return 'platform: ' + self.platform + ', friend_type: ' + self.friend_type + ', display_name: ' + self.display_name

class EventLog(models.Model):
    friend_id = models.ForeignKey('Friend')
    event_name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.event_name

class StateChat(models.Model):
    """
    StateChat is for keeping current chat state
    """
    
    STATEWAIT = 'WAIT'
    STATELEAVE = 'LEAVE'
    
    friend_id = models.ForeignKey('Friend')
    state = models.CharField(max_length=100,default='LEAVE')
    modified_date = models.DateTimeField(default=timezone.now)
    

    
    
    
    