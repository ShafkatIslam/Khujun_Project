# Generated by Django 2.2.4 on 2019-10-06 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Khujun', '0017_auto_20191006_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherprofile',
            name='images',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]