# Generated by Django 4.1.12 on 2024-02-13 19:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0016_remove_title_amount_title_books_per_box_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='placebook',
            name='added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
