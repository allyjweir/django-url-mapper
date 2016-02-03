# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='URLMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=64, verbose_name='Key', choices=[(b'terms-and-conditions', b'terms-and-conditions'), (b'awards', b'awards')])),
                ('url', models.CharField(help_text='Enter a relative URL', max_length=255, verbose_name='URL', blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='Object ID', blank=True)),
                ('view_name', models.CharField(max_length=255, verbose_name='View name', blank=True)),
                ('view_keywords', models.TextField(help_text='Use a=b to define keywords and commas to separate e.g slug=terms-and-conditions, language=en', verbose_name='View keywords', blank=True)),
                ('content_type', models.ForeignKey(verbose_name='Content Type', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name': 'URL map',
                'verbose_name_plural': 'URL maps',
            },
        ),
    ]
