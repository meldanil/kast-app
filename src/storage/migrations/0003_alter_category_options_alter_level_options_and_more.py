# Generated by Django 4.1.12 on 2023-10-11 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_alter_category_comment_alter_level_comment_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='level',
            options={'verbose_name_plural': 'Levels'},
        ),
        migrations.AlterModelOptions(
            name='place',
            options={'verbose_name_plural': 'Places'},
        ),
        migrations.AlterModelOptions(
            name='placebook',
            options={'verbose_name_plural': 'Placebooks'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'verbose_name_plural': 'Titles'},
        ),
        migrations.AlterField(
            model_name='title',
            name='cover',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
