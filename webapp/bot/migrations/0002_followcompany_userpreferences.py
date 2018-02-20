# Generated by Django 2.0.2 on 2018-02-20 21:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_code', models.CharField(max_length=6)),
                ('sector', models.CharField(max_length=40)),
                ('sub_sector', models.CharField(max_length=40)),
                ('current_price', models.BooleanField(default=True)),
                ('daily_high', models.BooleanField(default=True)),
                ('daily_low', models.BooleanField(default=True)),
                ('percentage_change', models.BooleanField(default=True)),
                ('news', models.BooleanField(default=False)),
                ('news_image', models.BooleanField(default=False)),
                ('last_time_got_news', models.DateField(verbose_name=datetime.date(2018, 2, 20))),
            ],
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colour_scheme', models.CharField(default='default', max_length=40)),
                ('voice_or_text', models.BooleanField(default=False)),
            ],
        ),
    ]
