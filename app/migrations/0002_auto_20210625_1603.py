# Generated by Django 3.2.4 on 2021-06-25 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserProfile',
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='UserProfile',
        ),
    ]