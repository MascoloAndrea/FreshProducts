# Generated by Django 4.0.2 on 2022-05-23 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_FreshProducts', '0006_alter_magazzino_scadenza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazzino',
            name='Scadenza',
            field=models.DateField(null=True, verbose_name='Scadenza'),
        ),
    ]
