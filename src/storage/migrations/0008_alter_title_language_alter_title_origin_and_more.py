# Generated by Django 4.1.12 on 2023-10-24 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0007_titlefile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='language',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='origin',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='publisher',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
