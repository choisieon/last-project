# Generated by Django 5.2.1 on 2025-06-23 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='badge',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
