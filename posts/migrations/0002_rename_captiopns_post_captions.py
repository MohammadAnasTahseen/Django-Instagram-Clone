# Generated by Django 4.2.5 on 2024-01-09 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='captiopns',
            new_name='captions',
        ),
    ]
