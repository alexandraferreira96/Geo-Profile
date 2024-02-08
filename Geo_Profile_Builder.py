# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# runs shapefiles
perfil = gpd.read_file("Perfil1.shp")
lito = gpd.read_file("lito_Perfil1.shp")

# isolar as coordenadas e projetar em gráfico
coord_perfil = perfil["geometry"]
coord_lito = lito["geometry"]

fig, ax = plt.subplots()
coord_perfil.plot(ax=ax, color='black', label='Perfil')
coord_lito.plot(ax=ax, marker='o', color='red', markersize=5, label='Sondagens')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
plt.legend(loc='best')

# calcular a distância à linha do perfil
def distancia_lito_perfil(coord_lito, coord_perfil): # litostratigrafia
    return coord_perfil.distance(coord_lito).min()
lito['Distância Perfil (m)'] = lito.geometry.apply(distancia_lito_perfil, args=(coord_perfil,))

# calcular a distância à origem
coord_furos = coord_perfil.geometry.boundary.explode(index_parts=True).unstack() # separa a linestring em multipoint e depois em point.
origem = coord_furos[0]

def distancia_lito_origem(coord_lito, origem):
    return origem.distance(coord_lito)
lito['Distância Origem (m)'] = lito.geometry.apply(distancia_lito_origem, args=(origem,))

# Cálculo da cota em profundidade de cada formação
lito['cota'] = lito['Topo'] - lito['profundida']

lito = lito.sort_values(by='Distância Origem (m)').reset_index(drop=True) # ordena a tabela pela distância à origem

cores = {
    'Aterros': '#d6d6d6', 'Aluviões': '#c5b0af', 'Calcários de Musgueira': '#ffc6d1',
    'Areias com Placuna miocénica': '#bcd166', 'Areias de Quinta do Bacalhau': '#67c600',
    'Calcários de Casal Vistoso': '#ff97b9', 'Argilas de Forno do Tijolo': '#81ffff',
    'Calcários de Entrecampos': '#ff1838', 'Areolas de Estefânia': '#ffc600',
    'Argilas de Prazeres': '#0566ff'} # atribui uma cor a cada formação, segundo o código HEX

fig, ax1 = plt.subplots() 
for nome, grupo in lito.groupby('NOME'):
    plt.scatter(grupo['Distância Origem (m)'], grupo['cota'], color=cores[nome], label=nome) # representação das formações
    #plt.plot(grupo['Distância Origem (m)'], grupo['cota'], '-o', color=cores[nome]) # representação dos limites
    plt.plot(lito['Distância Origem (m)'], lito['Topo'], color='black', label='Superfície') # representação da topografia
ax1.set_xlabel('Perfil (m)')
ax1.set_ylabel('Cota (m)')
ax1.axis('equal') # Coloca o perfil à escala real
# Criar a legenda para as classes com os nomes associados
legenda = [Line2D([0], [0], marker='o', color='w', markerfacecolor=cores[classe], markersize=10, label=nome_classe)
                   for classe, nome_classe in zip(lito['NOME'].unique(), lito['NOME'].unique())]
ax1.legend(handles=legenda, loc='upper center', title='Formações', bbox_to_anchor=(0.5, -0.05), ncol=4)

#%%
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

#correr as shapefiles
perfil = gpd.read_file("Perfil1_Perp.shp")
lito = gpd.read_file("lito_Perfil1_Perp.shp")

# isolar as coordenadas e projetar em gráfico
coord_perfil = perfil["geometry"]
coord_lito = lito["geometry"]

fig, ax = plt.subplots()
coord_perfil.plot(ax=ax, color='black', label='Perfil')
coord_lito.plot(ax=ax, marker='o', color='red', markersize=5, label='Sondagens')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
plt.legend(loc='best')

# calcular a distância à linha do perfil
def distancia_lito_perfil(coord_lito, coord_perfil): # litostratigrafia
    return coord_perfil.distance(coord_lito).min()
lito['Distância Perfil (m)'] = lito.geometry.apply(distancia_lito_perfil, args=(coord_perfil,))

# calcular a distância à origem
coord_furos = coord_perfil.geometry.boundary.explode(index_parts=True).unstack() # separa a linestring em multipoint e depois em point.
origem = coord_furos[0]

def distancia_lito_origem(coord_lito, origem):
    return origem.distance(coord_lito)

lito['Distância Origem (m)'] = lito.geometry.apply(distancia_lito_origem, args=(origem,))

# Cálculo da cota em profundidade de cada formação
lito['cota'] = lito['Topo'] - lito['profundida']

lito = lito.sort_values(by='Distância Origem (m)').reset_index(drop=True) # ordena a tabela pela distância à origem

cores = {
    'Aterros': '#999999',
    'Aluviões': '#a65628',
    'Areias de Quinta do Bacalhau': '#4daf4a',
    'Calcários de Casal Vistoso': '#f781bf',
    'Calcários de Musgueira': '#e41a1c',
    'Argilas de Forno do Tijolo': '#377eb8',
    'Areias com Placuna miocénica': '#ffff33',
} # atribui uma cor a cada formação, cores retiradas de https://colorbrewer2.org/#type=qualitative&scheme=Set3&n=9

fig, ax1 = plt.subplots() 
for nome, grupo in lito.groupby('NOME'):
    plt.scatter(grupo['Distância Origem (m)'], grupo['cota'], color=cores[nome], label=nome) # representação das formações
    #plt.plot(grupo['Distância Origem (m)'], grupo['cota'], '-o', color=cores[nome]) # representação dos limites
    plt.plot(lito['Distância Origem (m)'], lito['Topo'], color='black', label='Superfície') # representação da topografia
ax1.set_xlabel('Perfil (m)')
ax1.set_ylabel('Cota (m)')
#ax1.axis('equal') # Coloca o perfil à escala real
# Criar a legenda para as classes com os nomes associados
legenda = [Line2D([0], [0], marker='o', color='w', markerfacecolor=cores[classe], markersize=10, label=nome_classe)
                   for classe, nome_classe in zip(lito['NOME'].unique(), lito['NOME'].unique())]
ax1.legend(handles=legenda, loc='upper center', title='Formações', bbox_to_anchor=(0.5, -0.05), ncol=4)
