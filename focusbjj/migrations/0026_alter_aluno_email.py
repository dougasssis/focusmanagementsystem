# Generated by Django 4.0.4 on 2022-05-03 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focusbjj', '0025_aluno_is_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='email',
            field=models.EmailField(max_length=128),
        ),
    ]
