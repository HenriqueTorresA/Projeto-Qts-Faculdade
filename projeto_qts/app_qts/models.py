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

class Qts(models.Model):
    horario = models.CharField(max_length=10)
    domingo = models.CharField(max_length=100)
    segunda = models.CharField(max_length=100)
    terca = models.CharField(max_length=100)
    quarta = models.CharField(max_length=100)
    quinta = models.CharField(max_length=100)
    sexta = models.CharField(max_length=100)
    sabado = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.horario}: {self.segunda} - {self.terca} - {self.quarta} - {self.quinta} - {self.sexta} - {self.sabado} - {self.domingo}"