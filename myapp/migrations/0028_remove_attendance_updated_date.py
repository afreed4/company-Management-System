# Generated by Django 5.0.4 on 2024-09-06 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_attendance_attendence_date_attendance_updated_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='updated_date',
        ),
    ]
