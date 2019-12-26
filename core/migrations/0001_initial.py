# Generated by Django 3.0.1 on 2019-12-24 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('min_amount', models.PositiveIntegerField(default=0)),
                ('opened_date', models.DateTimeField(auto_now_add=True)),
                ('account_type', models.PositiveIntegerField(choices=[(0, 'Silver'), (1, 'Gold'), (2, 'Ordinary')], default=2)),
                ('monthly_fee', models.PositiveIntegerField(default=200)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('operation_type', models.PositiveIntegerField(choices=[(0, 'Deposit'), (1, 'Withdraw')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Account')),
            ],
        ),
    ]