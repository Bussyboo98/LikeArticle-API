# Generated by Django 3.2.3 on 2024-10-31 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='user',
        ),
    ]
