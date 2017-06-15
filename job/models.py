# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db import models
from django.utils import timezone
from steelframe.models import Friend

class Job(models.Model):
    
    COMMANDTYPEINTERNAL = 'INTERNAL'
    COMMANDTYPEEXTERNAL = 'EXTERNAL'
    
    JOBSTATUSWAITRUN = 'WAITRUN'
    JOBSTATUSRUNNING = 'RUNNING'
    JOBSTATUSWAITREPEAT = 'WAITREPEAT'
    JOBSTATUSCOMPLETED = 'COMPLETED'
    
    job_name = models.CharField(max_length=200)
    job_type = models.CharField(max_length=100)
    job_command = models.CharField(max_length=200)
    command_type = models.CharField(max_length=50)
    command_args = models.CharField(max_length=200)
    job_status = models.CharField(max_length=50)
    platform = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(null=True)
    modified_date = models.DateTimeField(default=timezone.now)
    modified_by = models.IntegerField(null=True)
    
    def __unicode__(self):
        return 'job_name: ' + self.job_name + ', job_command: ' + self.job_command + ', job_status: ' + self.job_status
 