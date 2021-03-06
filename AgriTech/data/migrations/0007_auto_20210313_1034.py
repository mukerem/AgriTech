# Generated by Django 3.1.7 on 2021-03-13 10:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20210313_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='item',
            name='farmer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='data.farmer'),
            preserve_default=False,
        ),
    ]
