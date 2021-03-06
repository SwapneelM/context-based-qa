# Generated by Django 2.0.1 on 2018-02-27 19:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Query')),
            ],
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colour_scheme', models.CharField(default='indigo', max_length=40)),
                ('company', models.CharField(max_length=6)),
                ('sector', models.CharField(max_length=40)),
                ('current_price', models.BooleanField(default=True)),
                ('daily_high', models.BooleanField(default=True)),
                ('daily_low', models.BooleanField(default=True)),
                ('percentage_change', models.BooleanField(default=True)),
                ('news', models.BooleanField(default=False)),
                ('voice', models.BooleanField(default=False)),
            ],
        ),
    ]
