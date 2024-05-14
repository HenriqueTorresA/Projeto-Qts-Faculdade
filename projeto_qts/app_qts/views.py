from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Aluno, Professor, Materia, Dia, Materia_Professor, Disponibilidade_Dia, Disponibilidade_Dia_Materia
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

# View responável por vincular matéria com professor e também realiza vinculo da matéria com o 
# dia da semana que o professor tem disponível 
def cadastrar_materia_professor(request):
    novo_mateira_professor = Materia_Professor()
    materiaId = request.POST.get('materia_id') # pega do HTML o elemento do nome materia_id
    professorId = request.POST.get('professor_id') # pega do HTML o elemento do nome professor_id
    # Obtém todos os vínculos de matéria com professor que já existem
    materiaProfessor = Materia_Professor.objects.all()
    
    # Não permitir que seja cadastrado um novo relacionamento de uma matéria que já tenha professor
    id_materia_lista = []
    for matprof in materiaProfessor: #Objeto que lista os vínculos existentes
        id_materia_lista.append(matprof.id_materia.id_materia) #Adiciona o id_materia na lista
    if int(materiaId) in id_materia_lista: #Se a matéria já existir nessa lista das matérias que já temos
        return redirect(tela_materia_professor) #Então voltar à tela de cadastro sem salvar nada

    # Lidar com o caso em que a matéria ou o professor não existe
    try:
        # Pegar a matéria que foi selecionada na tela
        materiaSelecionada = Materia.objects.get(pk=materiaId) 
        # Pegar o professor que foi selecionado na tela
        professorSelecionado = Professor.objects.get(pk=professorId)
    #Capturar a exceção que acusa que não existe valores em materia ou professor
    except (Materia.DoesNotExist, Professor.DoesNotExist):
        return render(request, 'qts/erros/erro_semProf_semId.html') # Retornar tela de erro
    # Se chegar até aqui, então salvar o novo registro de vínculo de matéria com professor
    novo_mateira_professor.id_materia = materiaSelecionada
    novo_mateira_professor.id_professor = professorSelecionado
    novo_mateira_professor.save()

    ##### Pegar o professor que foi vinculado com a matéria e vincular 
    ##### com os dias em que ele tem tem disponível
    disp_dia_prof = Disponibilidade_Dia.objects.all() #Obter os dias dos professores
    dias_completos = [c for c in disp_dia_prof] # Pegar todos os dias de todos os professores
    dias_prof = [] # Lista que armazenará somente os dias do professor que foi informado
    # Pegar a lista dos dias em que este professor tem disponibilidade
    for d in dias_completos: # Navegar pelos dias de todos os professores
        #Se chegar nos dias do professor que foi informado na tela, adicionar na lista dias_prof
        if str(d.id_professor.id_professor) == str(professorSelecionado.id_professor):
            dias_prof.append(d.id_dia)
    ### Vincular os dias do professor com o professor e a matéria selecionados
    cont = 0 # Contador que adicionará no for o id da disp. dia
    for d in dias_prof: # Percorrer a lista de dias do professor selecionado
        novo_disp_dia_prof_mat = Disponibilidade_Dia_Materia()
        novo_disp_dia_prof_mat.id_dia = d
        novo_disp_dia_prof_mat.id_materia = materiaSelecionada
        novo_disp_dia_prof_mat.id_professor = professorSelecionado
        print(f'Dias que está sendo cadastrado{novo_disp_dia_prof_mat.id_dia}')
        # VERIFICAR A POSSIBILIDADE DE VINCULAR O MATERIA_PROFESSOR COM A DISPON. DIA. MAT, AO 
        # INVÉS DE VINCULAR DIA, PROFESSOR, E MATÉRIA
        novo_disp_dia_prof_mat.save()
        cont += 1
    # Retornar à tela de cadastro
    return redirect(tela_materia_professor)

# View responsável por mostrar os vínculos de matéria com professor
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

# View responsável por deletar o vínculo de matéria com professor
def deletar_materia_professor(request, id_materia):
    materia_professor = get_object_or_404(Materia_Professor, id_materia=id_materia)
    materia_professor.delete()
    return redirect(listar_materia_professor)





#### ============================================================================================================
### FUNÇÕES QUE NÃO SÃO VIEWS

## Retorna os professores que não possuem vínculo com nenhuma matéria e também as matéria que 
## não possuem vínculo com nenhum professor
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
    # Retornar professores e matérias sem vínculos
    return professor_sem_vinculo, materia_sem_vinculo