# Generated by Django 3.1.7 on 2021-04-27 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('file_exchange', '0003_auto_20210421_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='user_id',
            field=models.ForeignKey(
                default=int,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='user_exercise',
                to='users.user'),
            preserve_default=False,
        ),
    ]
