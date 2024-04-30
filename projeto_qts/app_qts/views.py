from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno, Professor, Materia, Materia_Professor, Disponibilidade_Dia
# Create your views here.

def home(request): #nome que foi especificado no arquivos urls.py
    return render(request,'qts/home.html')

def tela_cadastrar_alunos(request):
    return render(request, 'qts/alunos_cadastro.html')
    
def cadastrar_alunos(request):
    novo_aluno = Aluno()
    novo_aluno.nome = request.POST.get('nome').strip()
    novo_aluno.login = request.POST.get('login').strip()
    novo_aluno.senha = request.POST.get('senha').strip()
    novo_aluno.save()
    return render(request,'qts/alunos_cadastro.html') 
    
def listar_alunos(request):
    # Exibir todos os alunos já cadastrados em uma nova página
    alunos = { # dicionário
        'alunos': Aluno.objects.all() # pega todos os objetos da classe Aluno
    }
    return render(request,'qts/alunos.html/',alunos) 

def deletar_alunos(request, id_aluno):
    aluno = get_object_or_404(Aluno, id_aluno=id_aluno)
    aluno.delete()
    return redirect(listar_alunos)

def tela_cadastrar_professores(request):
    return render(request, 'qts/professores_cadastro.html')

def cadastrar_professores(request):
    novo_professor = Professor()
    novo_professor.nome = request.POST.get('nome').strip()
    novo_professor.save()
    return render(request,'qts/professores_cadastro.html')

def cadastrar_disponibilidade_dia_professor(request, id_professor, id_dia):
    nova_materia_professor = Disponibilidade_Dia()
    nova_materia_professor.id_professor = id_professor
    nova_materia_professor.id_dia = id_dia
    nova_materia_professor.save()
    return render(request,'qts/professores_cadastro.html')

def listar_professores(request):
    professores = {
        'professores': Professor.objects.all()
    }
    return render(request,'qts/professores.html',professores)

def deletar_professores(request, id_professor):
    professor = get_object_or_404(Professor, id_professor=id_professor)
    professor.delete()
    return redirect(listar_professores)

def tela_cadastrar_materia(request):
    return render(request, 'qts/materias_cadastro.html')

def cadastrar_materia(request):
    nova_materia = Materia()
    nova_materia.nome = request.POST.get('nome').strip()
    nova_materia.save()
    return render(request,'qts/materias_cadastro.html')

def listar_materia(request):
    materia = {
        'materia': Materia.objects.all()
    }
    return render(request,'qts/materias.html',materia)

def deletar_materia(request, id_materia):
    materia = get_object_or_404(Materia, id_materia=id_materia)
    materia.delete()
    return redirect(listar_materia)

