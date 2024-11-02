# Generated by Django 5.1.2 on 2024-11-02 16:08

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("focusbjj", "0028_alter_aluno_photo_alter_aluno_stripe_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aluno",
            name="photo",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="photo"
            ),
        ),
    ]
