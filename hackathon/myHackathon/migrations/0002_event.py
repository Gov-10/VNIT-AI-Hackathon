# Generated by Django 5.1.7 on 2025-03-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myHackathon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=255)),
            ],
        ),
    ]
