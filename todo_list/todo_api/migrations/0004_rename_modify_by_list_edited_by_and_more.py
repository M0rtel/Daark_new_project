# Generated by Django 4.2.1 on 2023-05-30 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_api', '0003_task_is_public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='modify_by',
            new_name='edited_by',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='modify_by',
            new_name='edited_by',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='updated_at',
            new_name='updated',
        ),
    ]
