# Generated by Django 4.0.2 on 2022-04-27 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Licenze',
            fields=[
                ('Code', models.IntegerField(primary_key=True, serialize=False)),
                ('Data_sottoscrizione', models.DateTimeField(verbose_name='Data_sottoscrizione')),
                ('Data_scadenza', models.DateTimeField(verbose_name='Data_scadenza')),
                ('Prezzo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Prodotto',
            fields=[
                ('Barcode', models.IntegerField(primary_key=True, serialize=False)),
                ('Nome', models.CharField(max_length=200)),
                ('Marca', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Punto_vendita',
            fields=[
                ('Shop_code', models.AutoField(primary_key=True, serialize=False)),
                ('Nome', models.CharField(max_length=200)),
                ('Indirizzo', models.CharField(max_length=200)),
                ('Civico', models.CharField(max_length=200)),
                ('Citta', models.CharField(max_length=200)),
                ('Cap', models.IntegerField()),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_FreshProducts.licenze')),
            ],
        ),
        migrations.CreateModel(
            name='Magazzino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantita', models.IntegerField()),
                ('Reparto', models.CharField(max_length=200)),
                ('Prezzo', models.FloatField()),
                ('Scadenza', models.DateTimeField(verbose_name='Scadenza')),
                ('Barcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_FreshProducts.prodotto', unique=True)),
                ('Shop_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_FreshProducts.punto_vendita', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Credenziali',
            fields=[
                ('Username', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('Password', models.CharField(max_length=200)),
                ('Shop_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_FreshProducts.punto_vendita')),
            ],
        ),
    ]
