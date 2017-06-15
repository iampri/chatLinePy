# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from job.jobs import Jobs

def index(request):
    
    job = Jobs()
    res = job.run()
    
    return HttpResponse(res)

