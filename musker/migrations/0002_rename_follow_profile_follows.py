# Generated by Django 4.1.7 on 2023-03-17 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='follow',
            new_name='follows',
        ),
    ]
