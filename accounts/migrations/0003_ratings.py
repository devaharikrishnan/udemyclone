# Generated by Django 3.0.3 on 2020-02-12 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190420_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=200)),
                ('rating', models.IntegerField(default=0)),
                ('reviewedby', models.CharField(max_length=200)),
                ('courseid', models.CharField(max_length=200)),
            ],
        ),
    ]
