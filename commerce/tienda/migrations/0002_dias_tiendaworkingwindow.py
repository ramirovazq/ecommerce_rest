# Generated by Django 2.2.5 on 2019-09-22 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.SmallIntegerField(default=0)),
                ('dia', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='TiendaWorkingWindow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('dias', models.ManyToManyField(blank=True, to='tienda.Dias')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tienda.Tienda')),
            ],
        ),
    ]