# Generated by Django 4.0.4 on 2022-06-03 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConfessionsApp', '0011_confession_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='confession',
            name='edited_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]