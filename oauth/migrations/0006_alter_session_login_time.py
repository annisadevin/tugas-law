# Generated by Django 3.2.12 on 2022-03-10 12:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0005_alter_session_login_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='login_time',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
