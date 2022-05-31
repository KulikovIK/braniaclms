# Generated by Django 4.0.4 on 2022-05-31 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_coursefeedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursefeedback',
            name='rating',
            field=models.SmallIntegerField(choices=[(5, '⭐⭐⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (3, '⭐⭐⭐'), (2, '⭐⭐'), (1, '⭐')], default=5, verbose_name='Rating'),
        ),
    ]