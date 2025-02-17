# Generated by Django 5.0.7 on 2024-09-05 11:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Interval",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("cents", models.DecimalField(decimal_places=4, max_digits=10)),
                ("ratio_numerator", models.IntegerField(blank=True, null=True)),
                ("ratio_denominator", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Nomenclature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="System",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Scale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "root",
                    models.DecimalField(
                        blank=True, decimal_places=4, max_digits=10, null=True
                    ),
                ),
                ("intervals", models.ManyToManyField(to="pitches.interval")),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pitches.system"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="IntervalRole",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "interval",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pitches.interval",
                    ),
                ),
                (
                    "scale",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pitches.scale"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IntervalName",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("degree", models.IntegerField(blank=True, null=True)),
                (
                    "interval",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="additional_names",
                        to="pitches.interval",
                    ),
                ),
                (
                    "system",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pitches.system",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
