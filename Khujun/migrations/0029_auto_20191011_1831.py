# Generated by Django 2.2.6 on 2019-10-11 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Khujun', '0028_guardianprofile_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuitioninfo',
            name='guardian_confirm',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tuitioninfo',
            name='teacher_confirm',
            field=models.IntegerField(default=0),
        ),
    ]
