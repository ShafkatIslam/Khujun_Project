# Generated by Django 2.2.6 on 2019-10-11 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Khujun', '0027_teacherprofile_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardianprofile',
            name='notification',
            field=models.IntegerField(default=0),
        ),
    ]