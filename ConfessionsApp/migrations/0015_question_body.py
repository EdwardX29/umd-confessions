# Generated by Django 4.0.4 on 2022-06-03 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConfessionsApp', '0014_question_edited_question_edited_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='body',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]