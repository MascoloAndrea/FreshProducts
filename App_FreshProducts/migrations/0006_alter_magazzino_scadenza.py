# Generated by Django 4.0.2 on 2022-05-23 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_FreshProducts', '0005_alter_magazzino_scadenza_alter_punto_vendita_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazzino',
            name='Scadenza',
            field=models.DateTimeField(null=True, verbose_name='Scadenza'),
        ),
    ]
