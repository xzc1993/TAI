# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweeter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='screen_name',
            new_name='username',
        ),
    ]
