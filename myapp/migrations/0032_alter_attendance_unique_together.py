# Generated by Django 5.0.4 on 2024-09-07 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0031_remove_attendance_absent_remove_attendance_present_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('connection', 'attendence_date')},
        ),
    ]
