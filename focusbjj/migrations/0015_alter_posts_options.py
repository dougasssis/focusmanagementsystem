# Generated by Django 4.0.4 on 2022-04-19 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('focusbjj', '0014_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ['category', 'timestamp']},
        ),
    ]
