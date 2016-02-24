# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0002_imagelike_tag_userimageaction_usertaglike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagelike',
            name='image',
        ),
        migrations.DeleteModel(
            name='ImageLike',
        ),
        migrations.AddField(
            model_name='image',
            name='numberOfLikes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
