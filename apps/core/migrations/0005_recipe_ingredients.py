# Generated by Django 5.1.1 on 2024-10-26 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_ingredient'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='core.ingredient'),
        ),
    ]
