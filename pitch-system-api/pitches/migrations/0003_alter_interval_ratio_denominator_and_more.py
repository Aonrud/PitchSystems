# Generated by Django 5.0.7 on 2024-07-10 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pitches', '0002_alter_interval_ratio_denominator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interval',
            name='ratio_denominator',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='interval',
            name='ratio_enumerator',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
