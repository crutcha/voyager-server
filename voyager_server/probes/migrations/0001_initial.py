# Generated by Django 3.0.8 on 2020-07-31 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import netfields.fields
import uuid
from voyager_server.probes.models import Prober, ProbeTarget
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

def seed(apps, schema_editor):
    User = get_user_model()

    test_probe_user = User.objects.create_user(
        username="test-probe", is_staff=True, is_superuser=True, password="ChangeMe"
    )
    prober = Prober.objects.create(user=test_probe_user)
    target1 = ProbeTarget.objects.create(destination="8.8.8.8", interval=30, probe_count=10)
    target2 = ProbeTarget.objects.create(destination="1.1.1.1", interval=30, probe_count=10)
    target3 = ProbeTarget.objects.create(destination="cnn.com", interval=30, probe_count=10, type=3, port=443)
    prober.targets.add(target1)
    prober.targets.add(target2)

    Token.objects.create(user=test_probe_user)

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrefixInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asn', models.PositiveIntegerField(blank=True, null=True)),
                ('prefix', netfields.fields.CidrAddressField(max_length=43, unique=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=64)),
                ('country_code', models.CharField(max_length=3)),
                ('rir', models.CharField(blank=True, max_length=16, null=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'RIR'), (2, 'PRIVATE')])),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prober',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ProbeTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=64, unique=True)),
                ('interval', models.PositiveIntegerField()),
                ('probe_count', models.PositiveIntegerField(default=10)),
                ('port', models.PositiveIntegerField(blank=True, null=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'ICMP'), (2, 'UDP'), (3, 'TCP')], default=2)),
            ],
        ),
        migrations.CreateModel(
            name='ProbeResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('target', models.CharField(max_length=64)),
                ('probe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='probes.Prober')),
            ],
        ),
        migrations.AddField(
            model_name='prober',
            name='targets',
            field=models.ManyToManyField(to='probes.ProbeTarget'),
        ),
        migrations.AddField(
            model_name='prober',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ProbeHop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=64, null=True)),
                ('dns_name', models.CharField(max_length=128, null=True)),
                ('response_time', models.PositiveIntegerField()),
                ('ttl', models.PositiveIntegerField()),
                ('responded', models.BooleanField()),
                ('prefix', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='probes.PrefixInfo')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hops', to='probes.ProbeResult')),
            ],
        ),
        migrations.AddConstraint(
            model_name='prober',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='only 1 user per prober'),
        ),
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
