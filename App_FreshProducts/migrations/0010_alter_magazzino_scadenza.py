# Generated by Django 4.0.2 on 2022-05-24 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_FreshProducts', '0009_alter_magazzino_scadenza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazzino',
            name='Scadenza',
            field=models.DateField(null=True),
        ),
    ]
