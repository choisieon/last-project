# Generated by Django 5.2.1 on 2025-06-19 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_userprofile_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_image',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
