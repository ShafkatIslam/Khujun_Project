# Generated by Django 2.2.6 on 2019-10-07 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Khujun', '0021_auto_20191007_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardianprofile',
            name='email',
            field=models.TextField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='email',
            field=models.TextField(blank=True, max_length=50),
        ),
    ]
