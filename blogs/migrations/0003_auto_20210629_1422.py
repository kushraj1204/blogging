# Generated by Django 3.2.3 on 2021-06-29 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_blog_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='level',
        ),
        migrations.AddField(
            model_name='blog',
            name='version',
            field=models.IntegerField(default=0),
        ),
    ]
