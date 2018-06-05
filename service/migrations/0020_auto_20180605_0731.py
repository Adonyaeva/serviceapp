# Generated by Django 2.0.6 on 2018-06-05 07:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0019_auto_20180605_0731'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_name', models.CharField(max_length=200)),
                ('house_id', models.IntegerField()),
                ('house_number', models.IntegerField()),
                ('flat_number', models.IntegerField()),
                ('flat_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_full', models.CharField(max_length=400)),
                ('name_short', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('description', models.TextField()),
                ('estimate', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('status_id', models.IntegerField(default=0)),
                ('status_updated_time', models.DateTimeField(auto_now=True)),
                ('spent_time', models.IntegerField(default=0)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Address')),
                ('engineer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='service.Engineer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Service')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='service.Speciality')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField()),
                ('to_date', models.DateTimeField()),
                ('available', models.BooleanField()),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Engineer')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlotToEngineer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot_id', models.IntegerField()),
                ('engineer_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='time_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='service.TimeSlot'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='service',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Speciality'),
        ),
        migrations.AddField(
            model_name='engineer',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='service.Speciality'),
        ),
        migrations.AddField(
            model_name='engineer',
            name='time_slots',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='service.TimeSlot'),
        ),
    ]
