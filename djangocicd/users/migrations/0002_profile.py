# Generated by Django 4.0.7 on 2023-05-27 09:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posts_number', models.PositiveIntegerField(default=0)),
                ('subscriber_number', models.PositiveIntegerField(default=0)),
                ('subscription_number', models.PositiveIntegerField(default=0)),
                ('bio', models.TextField(blank=True, max_length=300, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
