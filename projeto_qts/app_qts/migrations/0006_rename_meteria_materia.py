# Generated by Django 5.0.4 on 2024-04-29 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_qts', '0005_dia_meteria_aluno_login_aluno_senha_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Meteria',
            new_name='Materia',
        ),
    ]