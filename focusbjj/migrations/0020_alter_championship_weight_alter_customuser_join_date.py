# Generated by Django 4.0.4 on 2022-04-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focusbjj', '0019_alter_championship_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championship',
            name='weight',
            field=models.CharField(choices=[('rooster', 'Rooster'), ('light feather', 'Light Feather'), ('feather', 'Feather'), ('light', 'Light'), ('middle', 'Middle'), ('middle heavy', 'Middle Heavy'), ('heavy', 'Heavy'), ('super heavy', 'Super Heavy'), ('ultra heavy', 'Ultra Heavy'), ('open', 'Open')], max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='join_date',
            field=models.DateTimeField(),
        ),
    ]