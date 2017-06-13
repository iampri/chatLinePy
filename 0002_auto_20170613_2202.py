# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 15:02
from __future__ import unicode_literals

from django.db import migrations

def create_initial_data(apps, schema_editor):
    Friend = apps.get_model("steelframe", "Friend")
    friend = Friend()
    friend.display_name = "PriewsFriends"
    friend.friend_type = "GROUP"
    friend.user_id = "Cd837b599d26fc150abe6133ab274fe95"
    friend.platform = "LINE"
    friend.save()
    
class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('steelframe', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]