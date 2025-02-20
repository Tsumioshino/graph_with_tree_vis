from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
from .forms import GrafoForm
from grafo.structs.Grafo import Grafo
from grafo.structs.req10 import Grafo_class, req10
grafo = Grafo()


def index(request):
  global grafo
  form = GrafoForm()
  context = {}
  print(request)
  if request.method == 'POST':
    if "botao_cria_grafo" in request.POST and len(request.POST.get("grafo_text")) > 0:
      grafo = Grafo()
      if request.POST.get('digrafo') == "on":
        grafo.digrafo = True
      if request.POST.get('digrafo') == "False":
        grafo.digrafo = False
      if request.POST.get('tree') == "on":
        grafo.tree = True
      if request.POST.get('tree') == "False":
        grafo.tree = False
      grafo.createDataFrame(request.POST.get("grafo_text"))
      grafo.imagem_bin["grafo"] = grafo.createImg()
    #R1
    if "botao_verifica_aresta" in request.POST:
      entrada = request.POST.get('vertice_aresta').split()
      if (request.POST.get('vertice_aresta') == ""):
        grafo.log.append(f"Há arestas no grafo: {grafo.containsAresta()}")
      elif (len(entrada) == 1):
        grafo.log.append(f"Há aresta no vertice {entrada[0]}: {grafo.containsAresta(entrada[0])}")
      else:
        grafo.log.append(f"Há aresta entre os vertices {entrada[0]} e {entrada[1]}: {grafo.containsAresta(entrada[0], entrada[1])}")
    #R2
    if "botao_verifica_grau" in request.POST:
      if len(request.POST.get('vertice_grau')) == 1:
        grafo.log.append(f"O Grau do Vertice {request.POST.get('vertice_grau')} é: {grafo.calcGrau(request.POST.get('vertice_grau'))}")
      else:
        grafo.log.append(f"R02 Input incorreto: {request.POST.get('vertice_grau')}")
    #R3
    if "botao_verifica_adj" in request.POST:
      if len(request.POST.get('vertice_adj')) == 1:
        grafo.log.append(f"Os vertices adjacentes são: {grafo.calcAdjacencia(request.POST.get('vertice_adj'))}")
      else:
        grafo.log.append(f"R03 Input incorreto: {request.POST.get('vertice_adj')}")
    #R4
    if "botao_grafo_nori_conexo" in request.POST:
      if grafo.digrafo:
        grafo.log.append("É um grafo orientado")
      else:
        grafo.log.append(f"O grafo não orientado é conexo?: {grafo.conexidadeGrafo()}")
    #R5
    if "botao_veri_digra_frac_conexo" in request.POST:
      if grafo.digrafo:
        if ("Fracamente Conexo" == grafo.conexidadeGrafo(force=True)):
          grafo.log.append(f"O grafo orientado é fracamente conexo?: True")
        else:
          grafo.log.append(f"O grafo orientado é fracamente conexo?: False")
      else:
        grafo.log.append("É um grafo não orientado")
    #R6
    if "botao_veri_digra_uni_conexo" in request.POST:
      if grafo.digrafo:
        grafo.log.append(f"O dígrafo é unilateralmente conexo?: {grafo.conexidadeGrafo(force=True)}")
      else:
        grafo.log.append("É um grafo não orientado")
    #R7
    if "botao_di_fort_conex" in request.POST:
      if grafo.digrafo:
        if ("Fortemente conexo" == grafo.conexidadeGrafo(force=True)):
          grafo.log.append(f"O dígrafo é fortemente conexo: {grafo.comp_forts()}")
        else:
          grafo.log.append(f"O grafo orientado não é fortemente conexo")
          grafo.log.append(f"Componentes: {grafo.comp_forts()}")
      else:
        grafo.log.append("É um grafo não orientado")
    #R8
    if "botao_graf_ciclo?" in request.POST:
      grafo.log.append(f"O grafo possui ciclo?: {grafo.hasCiclo()}")
    #R9
    if "botao_dig_aci_cone_ord_top" in request.POST:
      if (grafo.digrafo):
        if grafo.hasCiclo():
          grafo.log.append("Grafo possui ciclo")
        else:
          grafo.log.append(f"Calculando ordenação Topologica")
          grafo.ordenacaoTopologica()
      else:
        grafo.log.append("Grafo não orientado")
    #R10
    if "botao_veri_planar_2-con_eule" in request.POST:
      if grafo.conexidadeGrafo():
        resultado = req10(grafo.dataframe)
        for key in resultado:
          if(len(resultado[key][1]) != 0):
            grafo.log.append(f"{resultado[key]}")
          else:
            grafo.log.append(f"{resultado[key][0]}")
      else:
        grafo.log.append("Grafo desconexo")
    #R11
    if "botao_caminho_curto_custo" in request.POST:
      try:
        entrada = request.POST.get("short_path").split()
        if len(entrada) == 2:
          grafo.log.append(f"Calculando o caminho mais curto: {grafo.bellmanFord(entrada[0], entrada[1])}")
        else:
          grafo.log.append("Destino não inserido")
      except ValueError:
        grafo.log.append("R11 Impossivel encontrar caminho")
    #R12
    if "botao_arv_min" in request.POST:
      if not grafo.digrafo:
        grafo.log.append(f"Calculando arvore geradora minima")
        grafo.AGM()
      else:
        grafo.log.append("É um grafo orientado")
    if len(grafo.imagem_bin) != 0 and len(request.POST.get("grafo_text")) > 0:
      context["image"] = grafo.imagem_bin
    form.fields["grafo_text"].initial = request.POST.get('grafo_text')
    form.fields["digrafo"].initial = request.POST.get('digrafo')
    form.fields["tree"].initial = request.POST.get('tree')

    context['form'] = form
    context['grafo'] = grafo
  else:
    context = {
        'form': form,
        'image': None,
    }

  return render(request, "index.html", context)


def alunos(request):
  return render(request, "alunos.html")


def help(request):
  return render(request, "help.html")