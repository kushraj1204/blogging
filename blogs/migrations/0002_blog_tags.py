# Generated by Django 3.2.3 on 2021-06-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Tags'),
        ),
    ]
