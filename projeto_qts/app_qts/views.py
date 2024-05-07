from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno, Professor, Materia, Dia, Materia_Professor, Disponibilidade_Dia
# Create your views here.

def home(request): #nome que foi especificado no arquivos urls.py
    # Caso não existam dias na tabelas de dias da semana, adicionar dias sempre que o sistema for iniciado
    if not Dia.objects.exists():
        dias = ("Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado")
        for nome_dia in dias:
            dia = Dia(nome=nome_dia)
            dia.save()
    # Abrir a tela inicial home.html
    return render(request,'qts/home.html')

#abrir a tela de cadastro de alunos
def tela_cadastrar_alunos(request):
    return render(request, 'qts/cadastro/alunos_cadastro.html')
    
# View responsável por salvar o cadastro do novo aluno no model Aluno()
def cadastrar_alunos(request):
    novo_aluno = Aluno()
    novo_aluno.nome = request.POST.get('nome').strip()
    novo_aluno.login = request.POST.get('login').strip()
    novo_aluno.senha = request.POST.get('senha').strip()
    novo_aluno.save()
    return render(request,'qts/cadastro/alunos_cadastro.html') 
    
# Exibir todos os alunos já cadastrados no SQLite em uma nova página
def listar_alunos(request):
    alunos = { # cria um dicionário de alunos
        'alunos': Aluno.objects.all() # pega todos os objetos da classe Aluno
    }
    # inicia a página de listagem de alunos passando o dicionário como parâmetro
    # com isso o HTML poderá utilizar estes dados do dicionário para mostrá-lo na tela
    return render(request,'qts/listagem/alunos.html/',alunos) 
   
def deletar_alunos(request, id_aluno):
    aluno = get_object_or_404(Aluno, id_aluno=id_aluno)
    aluno.delete()
    return redirect(listar_alunos)

#abrir a tela de cadastro de alunos
def tela_cadastrar_professores(request):
    return render(request, 'qts/cadastro/professores_cadastro.html')

# View responsável por salvar o cadastro do novo professor no model Professor() e vincular com os dias
# no model Disponibilidade_Dia(), criando a disponibilidade dele
def cadastrar_professores(request):
    novo_professor = Professor()
    novo_professor.nome = request.POST.get('nome').strip()
    novo_professor.save()

    #Vincular o id_professor que acabou de salvar com os dias (id_dia) que ele possui disponibilidade
    dias_marcados = request.POST.getlist('dia[]')
    for dia_marcado in dias_marcados:
        disponibilidade = Disponibilidade_Dia()
        disponibilidade.id_professor = novo_professor
        dia = Dia.objects.get(id_dia=int(dia_marcado))
        disponibilidade.id_dia = dia
        disponibilidade.save()
    return render(request,'qts/cadastro/professores_cadastro.html')

#def cadastrar_disponibilidade_dia_professor(request, id_professor, id_dia):
#    nova_materia_professor = Disponibilidade_Dia()
#    nova_materia_professor.id_professor = id_professor
#    nova_materia_professor.id_dia = id_dia
#    nova_materia_professor.save()
#    return render(request,'qts/professores_cadastro.html')

def listar_professores(request):
    professores = {
        'professores': Professor.objects.all()
    }
    return render(request,'qts/listagem/professores.html',professores)

def deletar_professores(request, id_professor):
    professor = get_object_or_404(Professor, id_professor=id_professor)
    professor.delete()
    return redirect(listar_professores)

def tela_cadastrar_materia(request):
    return render(request, 'qts/cadastro/materias_cadastro.html')

def cadastrar_materia(request):
    nova_materia = Materia()
    nova_materia.nome = request.POST.get('nome').strip()
    nova_materia.save()
    return render(request,'qts/cadastro/materias_cadastro.html')

def listar_materia(request):
    materia = {
        'materia': Materia.objects.all()
    }
    return render(request,'qts/listagem/materias.html',materia)

def deletar_materia(request, id_materia):
    materia = get_object_or_404(Materia, id_materia=id_materia)
    materia.delete()
    return redirect(listar_materia)

def tela_materia_professor(request):
    context = {
        'professor': Professor.objects.all(),
        'materia': Materia.objects.all(),
        'materia_professor': Materia_Professor.objects.all()
    }
    return render(request, 'qts/vincular/materia_professor.html', context)
