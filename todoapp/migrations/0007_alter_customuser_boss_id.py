# Generated by Django 5.1.3 on 2025-03-16 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0006_alter_managertousertask_task_discreption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='boss_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
