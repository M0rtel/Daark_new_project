# Generated by Django 4.2.1 on 2023-05-29 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='old_version',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('DONE', 'Done'), ('PROCESS', 'Process'), ('CANCEL', 'Cancel')], max_length=20),
        ),
    ]
