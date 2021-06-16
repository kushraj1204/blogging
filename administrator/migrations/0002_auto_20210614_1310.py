# Generated by Django 3.2.3 on 2021-06-14 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='metadesc',
            field=models.TextField(blank=True, null=True, verbose_name='Homepage Meta Description'),
        ),
        migrations.AddField(
            model_name='settings',
            name='metakey',
            field=models.TextField(blank=True, null=True, verbose_name='Homepage Meta Key'),
        ),
    ]