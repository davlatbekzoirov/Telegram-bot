# Generated by Django 5.1 on 2024-08-13 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reffer_id', models.BigIntegerField(unique=True)),
                ('flag', models.BooleanField(default=False)),
                ('user_realy_name', models.CharField(max_length=255)),
            ],
        ),
    ]
