# Generated by Django 4.0.4 on 2022-06-03 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConfessionsApp', '0012_confession_edited_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confession',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='confession',
            name='edited_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
