# Generated by Django 5.2.1 on 2025-06-17 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentor', '0011_remove_question_curious_count_question_curious_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionview',
            name='viewed_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
