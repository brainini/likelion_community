# Generated by Django 3.2.5 on 2021-07-11 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college', models.CharField(blank=True, max_length=20, null=True)),
                ('major', models.CharField(blank=True, max_length=20, null=True)),
                ('batch', models.SmallIntegerField(blank=True, null=True)),
                ('tel', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('tmi', models.TextField()),
                ('github_id', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
