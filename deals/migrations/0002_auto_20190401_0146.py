# Generated by Django 2.1.7 on 2019-03-31 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='category',
            field=models.SmallIntegerField(choices=[(1, 'Appartment'), (2, 'Holiday home'), (3, 'Bed and breakfast')]),
        ),
    ]
