# Generated by Django 3.1 on 2020-08-10 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='CREATED', max_length=20),
        ),
    ]
