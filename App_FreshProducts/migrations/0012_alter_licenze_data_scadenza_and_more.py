# Generated by Django 4.0.2 on 2022-05-24 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_FreshProducts', '0011_alter_licenze_data_scadenza_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licenze',
            name='Data_scadenza',
            field=models.DateTimeField(verbose_name='Data_scadenza'),
        ),
        migrations.AlterField(
            model_name='licenze',
            name='Data_sottoscrizione',
            field=models.DateTimeField(verbose_name='Data_sottoscrizione'),
        ),
    ]
