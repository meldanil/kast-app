# Generated by Django 4.1.12 on 2023-10-12 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_alter_category_comment_alter_level_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storage.category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='level_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storage.level'),
        ),
    ]
