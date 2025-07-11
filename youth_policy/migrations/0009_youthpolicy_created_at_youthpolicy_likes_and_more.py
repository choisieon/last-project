# Generated by Django 5.2.1 on 2025-06-09 02:48

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youth_policy', '0008_policycomment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='youthpolicy',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youthpolicy',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_policies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='youthpolicy',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
