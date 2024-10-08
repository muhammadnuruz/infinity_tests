# Generated by Django 5.0.1 on 2024-08-05 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('words', '0003_words_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='words',
            name='category',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='words', to='categories.categories'),
            preserve_default=False,
        ),
    ]
