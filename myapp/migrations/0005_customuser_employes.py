# Generated by Django 5.0.4 on 2024-09-03 14:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_date_of_enquiry_companymanagement_date_of_registration'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='employes',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.companymanagement'),
            preserve_default=False,
        ),
    ]
