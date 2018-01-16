# Generated by Django 2.0 on 2018-01-16 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Photo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='full',
            field=models.URLField(default=None),
        ),
        migrations.AddField(
            model_name='photo',
            name='raw',
            field=models.URLField(default=None),
        ),
        migrations.AddField(
            model_name='photo',
            name='regular',
            field=models.URLField(default=None),
        ),
        migrations.AddField(
            model_name='photo',
            name='small',
            field=models.URLField(default=None),
        ),
        migrations.AddField(
            model_name='photo',
            name='thumb',
            field=models.URLField(default=None),
        ),
    ]
