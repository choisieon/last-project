# Generated by Django 5.2.1 on 2025-06-23 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_userprofile_badge'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='exp',
            field=models.IntegerField(default=0),
        ),
    ]
