# Generated by Django 3.0.2 on 2020-01-31 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20200130_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video_url',
            field=models.FileField(blank=True, null=True, upload_to='lessons/'),
        ),
    ]