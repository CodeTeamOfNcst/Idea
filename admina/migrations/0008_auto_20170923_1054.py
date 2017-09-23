# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-23 02:54
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('admina', '0007_auto_20170923_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e553a2-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e587f0-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='creation',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e4f48e-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='creation2projectlabel',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e50afa-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='follow',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e5a2c6-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='helpapplication',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e601d0-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e569d2-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='praise',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e53bf6-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e47b12-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='project2projectlabel',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e49f20-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='projectlabel',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e48e7c-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e4dde6-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='recruit',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e524ae-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e5bd10-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e5d872-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='scorechange',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e5ea2e-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e45ea2-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='user2userlabel',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e4c978-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
        migrations.AlterField(
            model_name='userlabel',
            name='Uuid',
            field=models.UUIDField(blank=True, default=uuid.UUID('81e4b276-a00a-11e7-8600-c03fd5f58c28'), null=True),
        ),
    ]
