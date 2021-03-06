# Generated by Django 4.0.4 on 2022-04-16 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focusbjj', '0006_graduation_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='category',
            field=models.CharField(blank=True, choices=[('newyear', 'Ano Novo'), ('xmas', 'Natal'), ('easter', 'Páscoa'), ('father', 'Dia dos Pais'), ('mother', 'Dia das Mães'), ('kids', 'Dia das Crianças'), ('women', 'Dia da Mulher'), ('others', 'Outros')], default='others', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='championship',
            name='category',
            field=models.CharField(choices=[('juvenil', 'Juvenil'), ('adult', 'Adulto/Master')], max_length=20),
        ),
        migrations.AlterField(
            model_name='championship',
            name='weight',
            field=models.CharField(choices=[('rooster', 'Rooster'), ('light feather', 'Light Feather'), ('feather', 'Feather'), ('light', 'Light'), ('middle', 'Middle'), ('middle_heavy', 'Middle Heavy'), ('heavy', 'Heavy'), ('super_heavy', 'Super Heavy'), ('ultra_heavy', 'Ultra Heavy'), ('open', 'Open')], max_length=20),
        ),
    ]
