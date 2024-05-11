from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
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
    context = {
        'materia': Materia.objects.all(),
        'materia_professor': Materia_Professor.objects.all()
    }
    return render(request,'qts/listagem/materias.html',context)

def deletar_materia(request, id_materia):
    materia = get_object_or_404(Materia, id_materia=id_materia)
    materia.delete()
    return redirect(listar_materia)

def tela_materia_professor(request):
    professores = Professor.objects.all()
    professor_sem_vinculo, materia_sem_vinculo = filtrar_prof_mat_sem_vinculo()
    context = {
        'professor': Professor.objects.all(),
        'professores_ids':[str(professor.id_professor) for professor in professores],
        'materia': Materia.objects.all(),
        'materia_professor': Materia_Professor.objects.all(),
        'materia_sem_vinculo': materia_sem_vinculo
    }
    return render(request, 'qts/vincular/materia_professor.html', context)

def cadastrar_materia_professor(request):
    novo_mateira_professor = Materia_Professor()
    materiaId = request.POST.get('materia_id')
    professorId = request.POST.get('professor_id')
    materiaProfessor = Materia_Professor.objects.all()
    # Não permitir que seja cadastrado um novo relacionamento de uma matéria que já tenha professor
    id_materia_lista = []
    for matprof in materiaProfessor:
        id_materia_lista.append(matprof.id_materia.id_materia)
    if int(materiaId) in id_materia_lista:
        return redirect(tela_materia_professor)

    # Lidar com o caso em que a matéria não existe
    try:
        materiaSelecionada = Materia.objects.get(pk=materiaId)
        professorSelecionado = Professor.objects.get(pk=professorId)
    except (Materia.DoesNotExist, Professor.DoesNotExist):
        return render(request, 'qts/vincular/materia_professor.html', {'mensagem': 'Matéria ou Professor não encontrada'})
  
    novo_mateira_professor.id_materia = materiaSelecionada
    novo_mateira_professor.id_professor = professorSelecionado
    novo_mateira_professor.save()

    return redirect(tela_materia_professor)

def listar_materia_professor(request):
    professor_sem_vinculo, materia_sem_vinculo = filtrar_prof_mat_sem_vinculo()

    context = {
        'professor': Professor.objects.all(),
        'materia': Materia.objects.all(),
        'materia_professor': Materia_Professor.objects.all(),
        'professor_sem_vinculo': professor_sem_vinculo,
        'materia_sem_vinculo': materia_sem_vinculo
    }
    return render(request, 'qts/listagem/materia_professor.html',context)

def deletar_materia_professor(request, id_materia):
    materia_professor = get_object_or_404(Materia_Professor, id_materia=id_materia)
    materia_professor.delete()
    return redirect(listar_materia_professor)





## ============================================================================================================
# FUNÇÕES QUE NÃO SÃO VIEWS
def filtrar_prof_mat_sem_vinculo():
    professor = Professor.objects.all()
    materia = Materia.objects.all()
    materia_professor = Materia_Professor.objects.all()

    # Extrai os IDs dos professores e materias vinculados
    professores_vinculados_ids = set([mp.id_professor.id_professor for mp in materia_professor])
    materias_vinculadas_ids = set([mp.id_materia.id_materia for mp in materia_professor])
    # Filtra os professores e materias que não estão vinculados
    professor_sem_vinculo = [prof for prof in professor if prof.id_professor not in professores_vinculados_ids]
    materia_sem_vinculo = [mat for mat in materia if mat.id_materia not in materias_vinculadas_ids]

    return professor_sem_vinculo, materia_sem_vinculo