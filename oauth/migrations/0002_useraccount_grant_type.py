# Generated by Django 3.2.12 on 2022-03-10 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='grant_type',
            field=models.CharField(default='password', max_length=10),
        ),
    ]