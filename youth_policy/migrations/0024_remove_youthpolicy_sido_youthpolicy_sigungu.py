# Generated by Django 5.2.1 on 2025-06-12 01:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youth_policy', '0023_alter_youthpolicy_sido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youthpolicy',
            name='sido',
        ),
        migrations.AddField(
            model_name='youthpolicy',
            name='sigungu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='youth_policy.sigungu'),
        ),
    ]
