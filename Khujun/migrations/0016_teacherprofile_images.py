# Generated by Django 2.2.4 on 2019-10-05 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Khujun', '0015_auto_20191006_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherprofile',
            name='images',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
