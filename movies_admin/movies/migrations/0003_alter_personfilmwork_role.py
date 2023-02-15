# Generated by Django 3.2.16 on 2023-02-15 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_add_fields_to_filmwork'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.TextField(choices=[('actor', 'actor'), ('director', 'director'), ('writer', 'writer')], default='actor', verbose_name='Role'),
        ),
    ]
