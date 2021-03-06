# Generated by Django 3.1.7 on 2021-05-05 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210503_0947'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='office',
            options={
                'permissions': [
                    ('alter_courses',
                     'Can alter course'),
                    ('create_courses',
                     'Can create course'),
                    ('delete_courses',
                     'Can delete course'),
                    ('manage_users',
                     'Can manage user'),
                    ('create_exercise',
                     'Can create exercises')]},
        ),
    ]
