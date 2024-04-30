from django.db import models

# Create your models here.

class Aluno(models.Model): #herda da classe models.Model
    id_aluno = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    login = models.TextField(max_length=50, default="sem login")
    senha = models.TextField(max_length=50, default="sem senha")

class Professor(models.Model):
    id_professor = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)

class Materia(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)

class Materia_Professor(models.Model):
    id_professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

class Dia(models.Model):
    id_dia = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)

class Disponibilidade_Dia(models.Model):
    id_professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    id_dia = models.ForeignKey(Dia, on_delete=models.CASCADE)

class Disponibilidade_Dia_Materia(models.Model):
    id_professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    id_dia = models.ForeignKey(Dia, on_delete=models.CASCADE)