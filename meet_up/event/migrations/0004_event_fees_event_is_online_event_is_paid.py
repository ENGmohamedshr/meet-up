# Generated by Django 5.1.1 on 2024-09-18 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_member_user_event_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='fees',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100, verbose_name='join fees'),
        ),
        migrations.AddField(
            model_name='event',
            name='is_online',
            field=models.BooleanField(default=False, verbose_name='online status'),
        ),
        migrations.AddField(
            model_name='event',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='is paid'),
        ),
    ]
