# Generated by Django 2.2.5 on 2019-10-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Khujun', '0008_auto_20191002_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardianregistration',
            name='nid',
            field=models.TextField(blank=True, max_length=15),
        ),
    ]
