# Generated by Django 2.2.4 on 2019-08-26 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='voip_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('received_count', models.IntegerField(default=0)),
                ('notes', models.TextField()),
            ],
        ),
    ]
