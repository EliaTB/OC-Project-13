# Generated by Django 2.1.7 on 2019-03-31 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='adult_nb',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='reservation',
            name='children_nb',
            field=models.SmallIntegerField(default=0),
        ),
    ]
