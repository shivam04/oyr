# Generated by Django 3.1 on 2020-08-09 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='isCustomr',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='aadhar_card',
            field=models.CharField(max_length=16),
        ),
    ]
