# Generated by Django 3.2.6 on 2021-08-06 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_activity_submission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='submissions',
        ),
        migrations.AddField(
            model_name='submission',
            name='activity_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='courses.activity'),
            preserve_default=False,
        ),
    ]
