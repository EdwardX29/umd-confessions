# Generated by Django 4.0.4 on 2022-05-21 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConfessionsApp', '0005_like_post_like_post_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_text',
            field=models.CharField(max_length=1666),
        ),
    ]
