# Generated by Django 4.0.4 on 2022-04-24 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focusbjj', '0022_alter_venda_aluno'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='time_stamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
