# Generated by Django 3.2.19 on 2023-07-09 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_request_vehicle_courier_assignment_unique_request_courier_vehicle'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='request_vehicle_courier_assignment',
            constraint=models.UniqueConstraint(fields=('RequestID', 'CourierID', 'VehicleID'), name='unique_request_courier_vehicle'),
        ),
    ]
