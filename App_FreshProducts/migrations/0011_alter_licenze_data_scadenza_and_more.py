# Generated by Django 4.0.2 on 2022-05-24 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_FreshProducts', '0010_alter_magazzino_scadenza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licenze',
            name='Data_scadenza',
            field=models.DateField(verbose_name='Data_scadenza'),
        ),
        migrations.AlterField(
            model_name='licenze',
            name='Data_sottoscrizione',
            field=models.DateField(verbose_name='Data_sottoscrizione'),
        ),
        migrations.AlterField(
            model_name='magazzino',
            name='Scadenza',
            field=models.DateField(blank=True, null=True),
        ),
    ]
