# Generated by Django 2.2.6 on 2019-10-07 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Khujun', '0023_tuitioninfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tuitioninfo',
            name='user',
        ),
        migrations.AddField(
            model_name='tuitioninfo',
            name='guardian_username',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]