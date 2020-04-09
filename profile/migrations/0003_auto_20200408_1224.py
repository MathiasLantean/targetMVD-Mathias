# Generated by Django 3.0.3 on 2020-04-08 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20200312_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, 'Gender Male'), (2, 'Gender Female'), (3, 'Gender Other')], null=True),
        ),
    ]
