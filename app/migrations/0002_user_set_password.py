# Generated by Django 5.2.1 on 2025-05-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='set_password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
