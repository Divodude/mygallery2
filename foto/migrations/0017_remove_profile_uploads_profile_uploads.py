# Generated by Django 4.2.15 on 2025-02-26 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foto', '0016_profile_uploads'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='uploads',
        ),
        migrations.AddField(
            model_name='profile',
            name='uploads',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='foto.dataset'),
        ),
    ]
