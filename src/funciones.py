# EXPLICIT Weights are listed explicitly in the corresponding section
# FULL MATRIX Weights are given by a full matrix
import networkx as nx
import numpy as np
import random

def matriz_init(filepath):
   with open(filepath, 'r') as file:
      lines = file.readlines()
   dimension = 0
   start_index = 0
   for i, line in enumerate(lines):
      if line.startswith("DIMENSION"):
         dimension = int(line.split(":")[1].strip())
      if line.strip() == "EDGE_WEIGHT_SECTION":
         start_index = i + 1
         break
   weights = []
   for line in lines[start_index:]:
      if line.strip() in ["EOF", ""]:
         break
      weights.extend(map(int, line.split()))
      
   matrix_np = np.array(weights).reshape((dimension, dimension))

   return matrix_np


filepath = './br17.atsp'
grafo = matriz_init(filepath)

print(grafo)
print("Forma de la matriz:", grafo.shape)


# HEURISTICA 1: algoritmo goloso: vecino mas cercano

def vecino_mas_cercano(matriz):
   nodo_0 = random.randint(0, matriz.shape[0]-1)
   nodos_visitados = [nodo_0]
   costo_viaje = 0
   
   while len(nodos_visitados) < matriz.shape[0]:
      min = (float('inf'), float('inf')) # nodo mas cercano, dist
      for i in range(matriz.shape[0]):
         dist_actual = matriz[nodo_0][i]
         if (dist_actual < min[1]) and (i not in nodos_visitados) and (dist_actual != 0):
            min = (i, dist_actual)
      nodos_visitados.append(min[0])
      nodo_0 = min[0]
      costo_viaje += min[1]
   
   print(nodos_visitados, costo_viaje)
   
vecino_mas_cercano(grafo)


def agm(matrix_np):
   # traduccion de matriz a grafo de nx
   g = nx.DiGraph()
   n = matrix_np.shape[0]
   g.add_nodes_from(range(n))
   for i in range(n):
      for j in range(n):
         if i!=j:
            if matrix_np[i, j] != 0:
               g.add_edge(i, j, weight=matrix_np[i, j])
   
   # Calcular el AGM usando Kruskal
   tree = nx.minimum_spanning_edges(g, algorithm='kruskal', data=True)

   # Crear un nuevo grafo para el MST
   k = nx.Graph()
   k.add_edges_from(tree)

   # Verificar el MST creado
   print("Aristas del MST:", k.edges(data=True))
   
agm(grafo)

