# Generated by Django 3.1.7 on 2021-04-27 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileexchange', '0004_submission_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='user_id',
            new_name='user',
        ),
    ]
