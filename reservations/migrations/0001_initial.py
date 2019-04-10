# Generated by Django 2.1.7 on 2019-04-10 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(0, 'Requested'), (1, 'Accepted'), (2, 'Refused')], null=True)),
                ('adult_nb', models.SmallIntegerField(default=1)),
                ('children_nb', models.SmallIntegerField(default=0)),
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to='deals.Deal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
