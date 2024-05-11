"""
URL configuration for projeto_qts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from app_qts import views

urlpatterns = [
    # rota, view responsável, nome de referência
    # facebook.com
    #path('')
    # facebook.com/devaprender --> O intúito desse path() é trazer tudo que vem depois do domínio
    #path('devaprender/')
    path('',views.home,name='home'),
    # quando o usuário entrar no site 127.0.0.1:8000/alunos/ o sistema vai levar ele para view de listar_alunos
    path('tela_cadastrar_alunos/',views.tela_cadastrar_alunos,name='tela_cadastrar_alunos'),
    path('cadastrar_alunos/',views.cadastrar_alunos,name="cadastrar_alunos"),
    path('listar_alunos/',views.listar_alunos,name='listar_alunos'),
    path('deletar_alunos/<int:id_aluno>',views.deletar_alunos,name='deletar_alunos'),
    path('tela_cadastrar_professores/',views.tela_cadastrar_professores,name="tela_cadastrar_professores"),
    path('cadastrar_professores/',views.cadastrar_professores,name="cadastrar_professores"),
    path('listar_professores/',views.listar_professores,name='listar_professores'),
    path('deletar_professores/<int:id_professor>',views.deletar_professores,name='deletar_professores'),
    path('tela_cadastrar_materia/',views.tela_cadastrar_materia,name="tela_cadastrar_materia"),
    path('cadastrar_materia/',views.cadastrar_materia,name="cadastrar_materia"),
    path('listar_materia/',views.listar_materia,name="listar_materia"),
    path('deletar_materia/<int:id_materia>',views.deletar_materia,name='deletar_materia'),
    path('tela_materia_professor',views.tela_materia_professor, name='tela_materia_professor'),
    path('cadastrar_materia_professor', views.cadastrar_materia_professor, name='cadastrar_materia_professor'),
    path('listar_materia_professor', views.listar_materia_professor, name='listar_materia_professor'),
    path('deletar_materia_professor/<int:id_materia>', views.deletar_materia_professor, name='deletar_materia_professor'),
]
