# Generated by Django 4.2.2 on 2023-06-11 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_article_readers_alter_userarticlerelation_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userarticlerelation',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations', to='articles.article', verbose_name='Статья'),
        ),
    ]
