# Generated by Django 3.0.8 on 2020-07-20 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProbeResult",
            fields=[
                (
                    "uuid",
                    models.CharField(max_length=36, primary_key=True, serialize=False),
                ),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("target", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="ProbeTarget",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("destination", models.CharField(max_length=64)),
                ("interval", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="ProbeHop",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hop", models.CharField(max_length=64)),
                ("response_time", models.PositiveIntegerField()),
                ("ttl", models.PositiveIntegerField()),
                ("responded", models.BooleanField()),
                (
                    "result",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="probes.ProbeResult",
                    ),
                ),
            ],
        ),
    ]
