from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno, Professor, Materia, Dia, Materia_Professor, Disponibilidade_Dia, Disponibilidade_Dia_Materia, Qts
import random
# Create your views here.

def home(request): #nome que foi especificado no arquivos urls.py
    # Caso não existam dias na tabelas de dias da semana, adicionar dias sempre que o sistema for iniciado
    if not Dia.objects.exists():
        dias = ("Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado")
        for nome_dia in dias:
            dia = Dia(nome=nome_dia)
            dia.save()
        gerar_qts()

    # Obter todas as disponibilidades e professores
    tabela_dados_gerais = gerar_quadro_geral()
    # Obter a tabela do QTS gerado randomicamente
    tabela_dados_qts = Qts.objects.all()
    # Definir o contexto
    contexto = {'tabela_dados_gerais': tabela_dados_gerais, 'tabela_dados_qts': tabela_dados_qts}

    return render(request, 'qts/home.html', contexto)
    
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
    todos_alunos = Aluno.objects.all() # Objetos alunos
    todos_alunos_ordenados = [] # receberá os alunos ordenados
    tabela_alunos = [] # Receberá a tabela a ser mostrada no tamplate

    ### ORDENANDO A LISTA DE ALUNOS
    # adicionando os alunos na lista a ser ordenada
    for als in todos_alunos:
        todos_alunos_ordenados.append(str(als.nome))
    # chamando o algoritmo quick sort
    todos_alunos_ordenados = ordena_nomes_quickSort(todos_alunos_ordenados)
    # Testando o resultado no terminal 
    print(f'Lista de alunos ordenada: \n  {todos_alunos_ordenados}')

    ### MONTANDO A TABELA DE ALUNOS
    for als_ord in todos_alunos_ordenados:
        for als in todos_alunos: # Comparar os alunos ordenados para mostrar os objetos
            if str(als_ord) == str(als.nome):
                tabela_alunos.append({
                    'id_aluno': als.id_aluno,
                    'nome': als.nome,
                    'login': als.login,
                    'senha': als.senha
                })

    context = {'tabela_alunos': tabela_alunos}
    return render(request,'qts/listagem/alunos.html/',context) 
   
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

def listar_professores(request):
    todos_professores = Professor.objects.all() # Objetos professores
    disponibilidade = Disponibilidade_Dia.objects.all()
    todos_prof_ordenados = [] # receberá os professores ordenados
    tabela_professores = [] # Receberá a tabela a ser mostrada no tamplate

    ### ORDENANDO A LISTA DE ALUNOS
    # adicionando os professores na lista a ser ordenada
    for prof in todos_professores:
        todos_prof_ordenados.append(str(prof.nome))
    # chamando o algoritmo quick sort
    todos_prof_ordenados = ordena_nomes_quickSort(todos_prof_ordenados)
    # Testando o resultado no terminal 
    print(f'Lista de professores ordenada: \n  {todos_prof_ordenados}')

    ### MONTANDO A TABELA DE ALUNOS
    for prof_ord in todos_prof_ordenados:
        for prof in todos_professores: # Comparar os professores ordenados para mostrar os objetos
            if str(prof_ord) == str(prof.nome):
                dias_disponiveis = [] # Iniciar os dias disponíveis deste professor
                for disp in disponibilidade:
                    if disp.id_professor.id_professor == prof.id_professor:
                        dias_disponiveis.append(f'{disp.id_dia.nome}/ ') # Adicionar os dias disponíveis
                tabela_professores.append({ # Montar a linha deste professor
                    'id_professor': prof.id_professor,
                    'nome': prof.nome,
                    'disponibilidade': ''.join(dias_disponiveis)
                })
    # Criar o Dicionário contendo as linhas da tabela
    context = {'tabela_professores': tabela_professores}

    return render(request,'qts/listagem/professores.html',context)

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
    
    todas_materias = Materia.objects.all() # Objetos materias
    todas_materias_ordenadas = [] # receberá as materias ordenadas
    tabela_materias = [] # Receberá a tabela a ser mostrada no tamplate

    ### ORDENANDO A LISTA DE MATERIAS
    # adicionando as materias na lista a ser ordenada
    for mat in todas_materias:
        todas_materias_ordenadas.append(str(mat.nome))
    # chamando o algoritmo quick sort
    todas_materias_ordenadas = ordena_nomes_quickSort(todas_materias_ordenadas)
    # Testando o resultado no terminal 
    print(f'Lista de materias ordenada: \n  {todas_materias_ordenadas}')

    ### MONTANDO A TABELA DE MATERIAS
    for mat_ord in todas_materias_ordenadas:
        for mat in todas_materias: # Comparar as materias ordenadas para mostrar os objetos
            if str(mat_ord) == str(mat.nome):
                tabela_materias.append({
                    'id_materia': mat.id_materia,
                    'nome': mat.nome
                })

    context = {'tabela_materias': tabela_materias}
    return render(request,'qts/listagem/materias.html',context)

def deletar_materia(request, id_materia):
    materia = get_object_or_404(Materia, id_materia=id_materia)
    materia.delete()
    return redirect(listar_materia)

def tela_materia_professor(request):
    professor_sem_vinculo, materia_sem_vinculo = filtrar_prof_mat_sem_vinculo()
    professores_ordenados_obj = obter_professores_ordenados()
    materias_ordenadas_obj = obter_materias_ordenadas()

    context = {
        'professor': professores_ordenados_obj,
        'materia': materias_ordenadas_obj,
        'materia_sem_vinculo': materia_sem_vinculo,
        'dia_professor': Disponibilidade_Dia.objects.all()

    }
    return render(request, 'qts/vincular/materia_professor.html', context)

# View responável por vincular matéria com professor e também realiza vinculo da matéria com o 
# dia da semana que o professor tem disponível 
def cadastrar_materia_professor(request):
    novo_mateira_professor = Materia_Professor()
    materiaId = request.POST.get('materia_id') # pega do HTML o elemento do nome materia_id
    professorId = request.POST.get('professor_id') # pega do HTML o elemento do nome professor_id
    diaId = request.POST.get('dia_id')
    dias_professor = []
    # Obtém todos os vínculos de matéria com professor que já existem
    materiaProfessor = Materia_Professor.objects.all()
    disp_dia = Disponibilidade_Dia.objects.all()
    for d in disp_dia:
        if int(d.id_professor.id_professor) == int(professorId):
            dias_professor.append(int(d.id_dia.id_dia))
    if int(diaId) not in dias_professor:
        return render(request, 'qts/erros/erro_semProf_semId.html')

    # Lidar com o caso em que a matéria ou o professor não existe
    try:
        # Pegar a matéria que foi selecionada na tela
        materiaSelecionada = Materia.objects.get(pk=materiaId) 
        # Pegar o professor que foi selecionado na tela
        professorSelecionado = Professor.objects.get(pk=professorId)
    #Capturar a exceção que acusa que não existe valores em materia ou professor
    except (Materia.DoesNotExist, Professor.DoesNotExist):
        return render(request, 'qts/erros/erro_semProf_semId.html') # Retornar tela de erro

    # Não permitir que seja cadastrado um novo relacionamento de uma matéria que já tenha professor
    # Desde que o vínculo que existe seja do mesmo professor que foi selecionado, em outro dia da semana
    teste = False # Teste que verifica se o professor selecionado é o mesmo do que já está vinculado com 
                  # esta matéria. Se for, então pode inserir a matéria, agora se não for, retornar o erro
                  # informando que a matéria já está vinculada a outro professor
    id_materia_lista = []
    for matprof in materiaProfessor: #Objeto que lista os vínculos existentes
        id_materia_lista.append(matprof.id_materia.id_materia) #Adiciona o id_materia na lista
        if matprof.id_materia == materiaSelecionada and matprof.id_professor == professorSelecionado:
            teste = True # Se o professor selecionado for o mesmo que já tem a matéria vinculada, permitir vínculo
    if int(materiaId) in id_materia_lista and not teste: #Se a matéria já existir nessa lista das matérias que já temos
        return render(request, 'qts/erros/erro_ja_tem_MateriaProfessor.html') #Então voltar à tela de cadastro sem salvar nada
    
    #pegar o id do dia selecionado em inteiro e gravar em uma variável do tipo objeto de dia
    for d in disp_dia:
        if int(d.id_dia.id_dia) == int(diaId):
            diaSelecionado = d.id_dia
    
    # Não permitir que seja cadastrado uma matéria com o professor em que o professor já esteja ocupado neste dia
    disp_prof_dia_mat = Disponibilidade_Dia_Materia.objects.all()
    dias_ocupados = [] # Lista para armazenar os dias do professor que estão ocupados
    for d in disp_prof_dia_mat:
        if d.id_professor.id_professor == professorSelecionado.id_professor:
            dias_ocupados.append(int(d.id_dia.id_dia)) # Add os dias que o prof já tem na Disponibilidade_Dia_Materia
    if int(diaSelecionado.id_dia) in dias_ocupados:
        return render(request, 'qts/erros/erro_professor_ocupado.html') # Retornar tela de erro do dia

    ##### Pegar o professor que foi vinculado com a matéria e vincular 
    ##### com o dia da semana escolhido
    novo_disp_dia_prof_mat = Disponibilidade_Dia_Materia()

    #Salvar o novo novo_disp_dia_prof_mat passando o prof, mat e o dia selecionado
    novo_disp_dia_prof_mat.id_dia = diaSelecionado
    novo_disp_dia_prof_mat.id_materia = materiaSelecionada
    novo_disp_dia_prof_mat.id_professor = professorSelecionado
    novo_disp_dia_prof_mat.save()    

    # Se chegar até aqui, então salvar o novo registro de vínculo de matéria com professor
    novo_mateira_professor.id_materia = materiaSelecionada
    novo_mateira_professor.id_professor = professorSelecionado
    novo_mateira_professor.save()


    return redirect(tela_materia_professor)

# View responsável por mostrar os vínculos de matéria com professor
def listar_materia_professor(request):
    professor_sem_vinculo, materia_sem_vinculo = filtrar_prof_mat_sem_vinculo()
    professores_ordenados_obj = obter_professores_ordenados()
    disp_dia_mat = Disponibilidade_Dia_Materia.objects.all()
    disp_dia_mat_ord = []
    for prof_ord in professores_ordenados_obj:
        for d in disp_dia_mat:
            if str(d.id_professor.nome) == str(prof_ord.nome):
                disp_dia_mat_ord.append(d)
    context = {
        'materia_professor_dia': disp_dia_mat_ord,
        'professor_sem_vinculo': professor_sem_vinculo,
        'materia_sem_vinculo': materia_sem_vinculo
    }
    return render(request, 'qts/listagem/materia_professor.html',context)

# View responsável por deletar o vínculo de matéria com professor
def deletar_materia_professor(request, id_materia):
    materia_professor = get_object_or_404(Materia_Professor, id_materia=id_materia)
    # Lógica responsável por realizar um "delete em cascata", ou seja, quando deletar o vínculo d eprof com mat, também vai deletar
    # o vínculo de prof com mat e com os dias
    disp_dia_mat_table = Disponibilidade_Dia_Materia.objects.all() # Lista de vínculo com professor, matéria, e dia da semana 
    disp_dia_mat = [d for d in disp_dia_mat_table] #Obtém os objetos da tabela Disponibilidade_Dia_Materia
    for c in disp_dia_mat: # Percorrer a lista de objetos
        if int(c.id_materia.id_materia) == int(materia_professor.id_materia.id_materia) and int(c.id_professor.id_professor) == int(materia_professor.id_professor.id_professor):
            c.delete()
    materia_professor.delete()
    return redirect(listar_materia_professor)

# View responsável por fazer a pesquisa do arquivo base e mostrar o resultado na tela de pesquisa.html
def pesquisa(request):
    # Criar objetos do banco
    obj_materias = Materia.objects.all()
    obj_professores = Professor.objects.all()
    obj_disp_dia_mat = Disponibilidade_Dia_Materia.objects.all()
    # Criar listas vazias para receber os valores
    materias = [] # Lista de todas as matérias
    professores = [] # Lista de todos os professores
    tabela_disp_dia_mat = []
    disponibilidade_dia_materia_mat = []
    materias_encontradas = []
    professores_encontrados = []
    disponibilidade_dia_materia_prof = []
    pesquisa = request.POST.get('pesquisa') # Valor digitado pelo usuário
    print(f"Pesquisa: \n{pesquisa}") # Debug do valor
    
    # Definir a lista de matérias e professores
    for mat in obj_materias: 
        materias.append(mat.nome)
    for prof in obj_professores: 
        professores.append(prof.nome)
    for disp in obj_disp_dia_mat:
        disponibilidade_dia_materia_mat.append(disp.id_materia.nome)
        disponibilidade_dia_materia_prof.append(disp.id_professor.nome)
        
    # Ordenar em ordem alfabética a lista de matérias e professores
    materias = ordena_nomes_quickSort(materias)
    professores = ordena_nomes_quickSort(professores)
    disponibilidade_dia_materia_mat = ordena_nomes_quickSort(disponibilidade_dia_materia_mat)
    disponibilidade_dia_materia_prof = ordena_nomes_quickSort(disponibilidade_dia_materia_prof)

    # Executar o algoritmo de busca binária usando as listas ordenadas
    busca_materias = buscaBinaria(materias, pesquisa, 0, len(materias)-1)
    busca_professores = buscaBinaria(professores, pesquisa, 0, len(professores)-1)
    #Procurar matérias dentro da disponibilidade_dia_materia
    for d in obj_disp_dia_mat:
        if str(d.id_materia.nome) == str(pesquisa):
            materias_encontradas.append(d)
    #Procurar professores dentro da disponibilidade_dia_materia
    for d in obj_disp_dia_mat:
        if str(d.id_professor.nome) == str(pesquisa):
            professores_encontrados.append(d)

    # procurar o resultado da busca na lista de objetos do banco da tabela de matérias
    if busca_materias >= 0: # Garantir que o valor do retorno da função não seja -1
        for mat in obj_materias:
            # Comparar o elemento do indice retornado pelo algoritmo, da lista ordenada
            # com os elementos que temos da lista de obejtos do banco, para garantir que 
            # o valor procurado está no banco 
            if str(mat.nome) == str(materias[busca_materias]): 
                obj_materia_encontrada_nome = mat.nome
                obj_materia_encontrada_id = mat.id_materia
    else: # Se o retorno da função for -1 significa que não encontrou o valor
        # (tratar isso no HTML do Django)
        obj_materia_encontrada_nome = 'naoencontrado'
        obj_materia_encontrada_id = 'naoencontrado'

    # procurar o resultado da busca na lista de objetos do banco da tabela de professores
    if busca_professores >= 0: # Garantir que o valor do retorno da função não seja -1
        for prof in obj_professores:
            # Comparar o elemento do indice retornado pelo algoritmo, da lista ordenada
            # com os elementos que temos da lista de obejtos do banco, para garantir que 
            # o valor procurado está no banco 
            if str(prof.nome) == str(professores[busca_professores]): 
                obj_professor_encontrado_nome = prof.nome
                obj_professor_encontrado_id = prof.id_professor
    else: # Se o retorno da função for -1 significa que não encontrou o valor
        # (tratar isso no HTML do Django)
        obj_professor_encontrado_nome = 'naoencontrado'
        obj_professor_encontrado_id = 'naoencontrado'

    # Montar as listas de dicionários e montar as tabelas que vão ser apresentadas no HTML
    tabela_materia = [{'id': obj_materia_encontrada_id, 'nome': obj_materia_encontrada_nome}]
    tabela_professor = [{'id': obj_professor_encontrado_id, 'nome': obj_professor_encontrado_nome}]
    for mat in materias_encontradas: # Matérias encontradas na disponibilidade_dia_materia
        tabela_disp_dia_mat.append({
            'nome_materia': mat.id_materia.nome,
            'nome_professor': mat.id_professor.nome,
            'nome_dia': mat.id_dia.nome
        })
    for prof in professores_encontrados: # Professores encontrados na disponibilidade_dia_materia
        tabela_disp_dia_mat.append({
            'nome_materia': prof.id_materia.nome,
            'nome_professor': prof.id_professor.nome,
            'nome_dia': prof.id_dia.nome
        })

    # Montar o dicionário principal do contexto para enviar as informações ao HTML
    contexto = {'tabela_professor': tabela_professor, 
                'tabela_materia': tabela_materia,
                'tabela_disp_dia_mat': tabela_disp_dia_mat}

    return render(request, 'qts/pesquisa.html', contexto)

# View que chama a função de gerar_qts
def botao_gerar_qts(request):
    gerar_qts()
    return redirect(home)

#### ============================================================================================================
### FUNÇÕES QUE NÃO SÃO VIEWS

# Gera o quadro geral de matérias e professores com vínculo na tela inicial
def gerar_quadro_geral():
    disp_dia_mat = Disponibilidade_Dia_Materia.objects.all()
    professores = Professor.objects.all()
    professores_ordenados = [] # Armazena a lista de nome dos professores, porém de forma ordenada
    professores_ordenados_obj = [] # Armazena os objetos do tipo Professor, de forma ordenada por nome
    tabela_dados_gerais = [] # Armazena as linhas da tabela de dados gerais

    for prof in professores: # Colocar o nome de todos os professores na lista que vamos ordenar
        professores_ordenados.append(str(prof.nome))
    professores_ordenados = ordena_nomes_quickSort(professores_ordenados) #Ordenar a lista de nomes
    for p in professores_ordenados: # Percorrer a lista de nome dos professores ordenados
        for prof in professores: # Percorrer a lista de objetos para ordenar essa lista
            if str(prof.nome) == p: # Adicionar o objeto se o nome for igual ao nome atual da lista ordenada
                professores_ordenados_obj.append(prof) # Montar a lista ordenada por nome dos objetos
    
    # GERAR A TABELA GERAL
    for prof in professores_ordenados_obj:
        # Inicializa um dicionário para armazenar as matérias de cada dia da semana para o professor atual
        professor_atual = {dia: "-" for dia in range(1, 8)} # Inicializa todos os dias com "-"
        for disp in disp_dia_mat:
            if disp.id_professor.id_professor == prof.id_professor:
                # Atualiza o dia específico com a matéria correta
                professor_atual[disp.id_dia.id_dia] = disp.id_materia.nome
        # Adiciona os dados do professor atual à tabela
        tabela_dados_gerais.append({
            'professor': prof.nome,
            'domingo': professor_atual[1],
            'segunda': professor_atual[2],
            'terca': professor_atual[3],
            'quarta': professor_atual[4],
            'quinta': professor_atual[5],
            'sexta': professor_atual[6],
            'sabado': professor_atual[7]
        })
        # Debug: imprime as disponibilidades para cada professor
        print(f'Professor: {prof.nome}, Domingo: {professor_atual[1]}'+
              f'Segunda: {professor_atual[2]}, Terça: {professor_atual[3]},' +
              f'Quarta: {professor_atual[4]}, Quinta: {professor_atual[5]},' +
              f'Sexta: {professor_atual[6]}, Sábado: {professor_atual[7]}')
    return tabela_dados_gerais

# Gera o QTS de forma randômica e o armazena no banco
def gerar_qts():
    tabela_dados_qts = [] # Armazena as linhas da tabela de QTS
    # Define de forma estática a quantidade de horários que possuem na instituição
    horarios = ['1º', '2º', '3º', '4º']
    Qts.objects.all().delete()
    # Cria 4 linhas para a tabela do QTS
    for i in horarios:
        horario_atual = {dia: "-" for dia in range(1, 8)} # Preenche todas as colunas com valor default
        for j in range(1, 8):
            obj_dia = sortear_materia(j) # Sorteia a matéria do dia
            if obj_dia is not None:
                # Adiciona a matéria no horário, somente se a lista de matérias do dia for > 0
                horario_atual[j] = f'{obj_dia.id_materia.nome} - {obj_dia.id_professor.nome}'
        # Montar a linha do horário atual da tabela de matérias do QTS
        linha_qts = {
            'horario': i,
            'domingo': horario_atual[1],
            'segunda': horario_atual[2],
            'terca': horario_atual[3],
            'quarta': horario_atual[4],
            'quinta': horario_atual[5],
            'sexta': horario_atual[6],
            'sabado': horario_atual[7]
        }
        tabela_dados_qts.append(linha_qts) # Adicionar lista da tabela
        Qts.objects.create(**linha_qts ) #Adicionar linha no banco SQLite

    #Qts.tabela_qts = tabela_dados_qts
    return tabela_dados_qts

# Sorteia a matéria do dia quando vai gerar o QTS (de forma randômica)
def sortear_materia(id_dia):
    disp_dia_mat = Disponibilidade_Dia_Materia.objects.all()
    # Definir as listas de matérias por dia da semana
    materias_domingo = [d for d in disp_dia_mat if (d.id_dia.id_dia) == 1]
    materias_segunda = [d for d in disp_dia_mat if (d.id_dia.id_dia) == 2]
    materias_terca = [d for d in disp_dia_mat if (d.id_dia.id_dia) == 3]
    materias_quarta = [d for d in disp_dia_mat if (d.id_dia.id_dia) == 4]
    materias_quinta = [d for d in disp_dia_mat if (d.id_dia.id_dia) == 5]
    materias_sexta = [d for d in disp_dia_mat if (d.id_dia.id_dia) == 6]
    materias_sabado = [d for d in disp_dia_mat if (d.id_dia.id_dia) == 7]
    # Retornar a lista do dia que foi solicitado 
    if int(id_dia) == 1 and len(materias_domingo) > 0:
        return random.choice(materias_domingo)
    if int(id_dia) == 2 and len(materias_segunda) > 0:
        return random.choice(materias_segunda)
    if int(id_dia) == 3 and len(materias_terca) > 0:
        return random.choice(materias_terca)
    if int(id_dia) == 4 and len(materias_quarta) > 0:
        return random.choice(materias_quarta)
    if int(id_dia) == 5 and len(materias_quinta) > 0:
        return random.choice(materias_quinta)
    if int(id_dia) == 6 and len(materias_sexta) > 0:
        return random.choice(materias_sexta)
    if int(id_dia) == 7 and len(materias_sabado) > 0:
        return random.choice(materias_sabado)

# Retorna os professores que não possuem vínculo com nenhuma matéria e também as matéria que 
# não possuem vínculo com nenhum professor
def filtrar_prof_mat_sem_vinculo():
    professor = Professor.objects.all()
    professor_ordenado = obter_professores_ordenados()
    materia_ordenada = obter_materias_ordenadas()
    materia = Materia.objects.all()
    materia_professor = Materia_Professor.objects.all()

    # Extrai os IDs dos professores e materias vinculados
    professores_vinculados_ids = set([mp.id_professor.id_professor for mp in materia_professor])
    materias_vinculadas_ids = set([mp.id_materia.id_materia for mp in materia_professor])
    # Filtra os professores e materias que não estão vinculados
    professor_sem_vinculo = [prof for prof in professor if prof.id_professor not in professores_vinculados_ids]
    materia_sem_vinculo = [mat for mat in materia if mat.id_materia not in materias_vinculadas_ids]
    professor_sem_vinculo_ord = []
    materia_sem_vinculo_ord = []
    # Ordenar a lista de professores sem vínculo
    for po in professor_ordenado:
        for p in professor_sem_vinculo:
            if str(po.nome) == str(p.nome):
                professor_sem_vinculo_ord.append(p)
    # Ordenar a lista de matérias sem vínculo
    for mo in materia_ordenada:
        for m in materia_sem_vinculo:
            if str(mo.nome) == str(m.nome):
                materia_sem_vinculo_ord.append(m)

    # Retornar professores e matérias sem vínculos
    return professor_sem_vinculo_ord, materia_sem_vinculo_ord
    
# Algoritmo de busca binária
# Retorna o índice do valor procurado dentro da lista passada
def buscaBinaria(lista_palavras, palavra, primeiro, ultimo):
    if primeiro <= ultimo:
        meio = (primeiro + ultimo) // 2
        if lista_palavras[meio] == palavra:
            return meio
        elif lista_palavras[meio] < palavra:
            return buscaBinaria(lista_palavras, palavra, meio + 1, ultimo)
        else:
            return buscaBinaria(lista_palavras, palavra, primeiro, meio - 1)
    else:
        return -1 # Retornar -1 caso não exista valores iguais ao procurado

# Algoritmo de ordeção quickSort
# Retorna a mesma lista que foi passada, porém ordenada (serve para strings)
def ordena_nomes_quickSort(array_list):
    
    if len(array_list) <= 1:
        return array_list
    
    pivo = array_list[0]
    menores = [x for x in array_list[1:] if x < pivo]
    iguais = [x for x in array_list[1:] if x == pivo]
    maiores = [x for x in array_list[1:] if x > pivo]
    
    return ordena_nomes_quickSort(menores) + [pivo] + iguais + ordena_nomes_quickSort(maiores)

# Busca os objetos de professores ordenados por nome
# Retorna os objetos de professores ordenados por nome
def obter_professores_ordenados():
    professores = Professor.objects.all()
    professores_ordenados = [] # Armazena a lista de nome dos professores, porém de forma ordenada
    professores_ordenados_obj = [] # Armazena os objetos do tipo Professor, de forma ordenada por nome

    for prof in professores: # Colocar o nome de todos os professores na lista que vamos ordenar
        professores_ordenados.append(str(prof.nome))
    professores_ordenados = ordena_nomes_quickSort(professores_ordenados) #Ordenar a lista de nomes
    for p in professores_ordenados: # Percorrer a lista de nome dos professores ordenados
        for prof in professores: # Percorrer a lista de objetos para ordenar essa lista
            if str(prof.nome) == p: # Adicionar o objeto se o nome for igual ao nome atual da lista ordenada
                professores_ordenados_obj.append(prof) # Montar a lista ordenada por nome dos objetos
    
    return professores_ordenados_obj

# Busca os objetos de materias ordenados por nome
# Retorna os objetos de materias ordenados por nome
def obter_materias_ordenadas():
    materias = Materia.objects.all()
    materias_ordenadas = [] # Armazena a lista de nome das materias, porém de forma ordenada
    materias_ordenadas_obj = [] # Armazena os objetos do tipo Professor, de forma ordenada por nome

    for mat in materias: # Colocar o nome de todas os materias na lista que vamos ordenar
        materias_ordenadas.append(str(mat.nome))
    materias_ordenadas = ordena_nomes_quickSort(materias_ordenadas) #Ordenar a lista de nomes
    for m in materias_ordenadas: # Percorrer a lista de nome das materias ordenadas
        for mat in materias: # Percorrer a lista de objetos para ordenar essa lista
            if str(mat.nome) == str(m): # Adicionar o objeto se o nome for igual ao nome atual da lista ordenada
                materias_ordenadas_obj.append(mat) # Montar a lista ordenada por nome das objetos
    return materias_ordenadas_obj