# Generated by Django 2.2.5 on 2019-09-22 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Khujun', '0002_auto_20190922_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherregistration',
            name='ssc_roll',
            field=models.IntegerField(blank=True, max_length=6, verbose_name="Student's Roll"),
        ),
    ]
