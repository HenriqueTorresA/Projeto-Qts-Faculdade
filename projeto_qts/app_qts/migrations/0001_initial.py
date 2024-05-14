# Generated by Django 5.0.4 on 2024-05-14 05:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id_aluno', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.TextField(max_length=255)),
                ('login', models.TextField(default='sem login', max_length=50)),
                ('senha', models.TextField(default='sem senha', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Dia',
            fields=[
                ('id_dia', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id_materia', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id_professor', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Materia_Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_qts.materia')),
                ('id_professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_qts.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Disponibilidade_Dia_Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_dia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_qts.dia')),
                ('id_materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_qts.materia')),
                ('id_professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_qts.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Disponibilidade_Dia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_dia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_qts.dia')),
                ('id_professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_qts.professor')),
            ],
        ),
    ]
