# Generated by Django 3.1 on 2020-08-23 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Номер поезда')),
                ('travel_time', models.IntegerField(verbose_name='Время в пути')),
                ('from_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_city', to='cities.city', verbose_name='Откуда')),
                ('to_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_city', to='cities.city', verbose_name='Куда')),
            ],
            options={
                'verbose_name': 'Поезд',
                'verbose_name_plural': 'Поезда',
                'ordering': ['name'],
            },
        ),
    ]
