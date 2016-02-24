# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0003_auto_20150508_0552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hiclothuser',
            name='user',
        ),
        migrations.AlterField(
            model_name='userimageaction',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usertaglike',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='HiClothUser',
        ),
    ]
