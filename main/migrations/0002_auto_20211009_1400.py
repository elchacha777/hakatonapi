# Generated by Django 3.1 on 2021-10-09 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lostitem',
            name='status',
            field=models.CharField(choices=[('lost', 'lost'), ('found', 'found')], max_length=10),
        ),
    ]
