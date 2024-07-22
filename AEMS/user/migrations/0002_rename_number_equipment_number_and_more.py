# Generated by Django 5.0.7 on 2024-07-20 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment',
            old_name='Number',
            new_name='number',
        ),
        migrations.AlterField(
            model_name='booking',
            name='phone_number',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        migrations.DeleteModel(
            name='Bill',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
    ]
