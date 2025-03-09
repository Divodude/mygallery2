# Generated by Django 4.2.15 on 2025-03-04 17:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foto', '0022_remove_profile_embedding'),
    ]

    operations = [
        migrations.CreateModel(
            name='clubdb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True)),
                ('image', models.FileField(upload_to='club/')),
                ('members', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
