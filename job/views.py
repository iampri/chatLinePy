# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from job.jobs import Jobs

def index(request):
    
    job = Jobs()
    job.run()
    
    return HttpResponse('oki')

