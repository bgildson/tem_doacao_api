# Generated by Django 2.2.8 on 2019-12-18 00:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('at', models.DateTimeField(auto_now_add=True)),
                ('donation', models.ForeignKey(db_column='donation_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favorites', to='donations.Donation')),
                ('user', models.ForeignKey(db_column='user_id_donor', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]