# Generated by Django 2.2.4 on 2019-10-06 07:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Khujun', '0019_delete_teacherimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuardianProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.TextField(blank=True, max_length=50)),
                ('gender_name', models.CharField(blank=True, max_length=200)),
                ('blood_group', models.CharField(blank=True, max_length=200)),
                ('address', models.TextField(blank=True, max_length=50)),
                ('city', models.TextField(blank=True, max_length=50)),
                ('nid', models.TextField(blank=True, max_length=17)),
                ('images', models.TextField(blank=True, max_length=1000, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]