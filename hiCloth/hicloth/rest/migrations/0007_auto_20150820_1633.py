# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0006_auto_20150810_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relType', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='isChecked',
        ),
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(default=b'none', max_length=200),
        ),
        migrations.AddField(
            model_name='tagrelationship',
            name='firstTag',
            field=models.ForeignKey(related_name='firstTag', to='rest.Tag'),
        ),
        migrations.AddField(
            model_name='tagrelationship',
            name='secondTag',
            field=models.ForeignKey(related_name='secondTag', to='rest.Tag'),
        ),
    ]
