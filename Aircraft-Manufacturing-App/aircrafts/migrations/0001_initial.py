# Generated by Django 5.2.1 on 2025-05-19 05:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('aircreaft_type', models.CharField(choices=[('TB2', 'TB2'), ('TB3', 'TB3'), ('Akinci', 'Akinci'), ('Kizilelme', 'Kizilelma')], max_length=20)),
                ('assembled_at', models.DateTimeField(auto_now_add=True)),
                ('assembled_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('avionics', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='used_as_avionics', to='parts.part')),
                ('fuselage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='used_as_fuselage', to='parts.part')),
                ('tail', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='used_as_tail', to='parts.part')),
                ('wing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='used_as_wing', to='parts.part')),
            ],
        ),
    ]
