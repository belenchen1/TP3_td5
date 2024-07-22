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

#print(grafo)
print("Forma de la matriz:", grafo.shape)

# HEURISTICA 1: algoritmo goloso: vecino mas cercano
def vecino_mas_cercano(matriz):
   '''Hay veces que el camino que construye no es valido. Por eso hacemos el ciclo externo sirve para comenzar de nuevo opciones de caminos
   
   Complejidad total:  O(N**2)
      O (1) (ciclo externo)
         O(n) (ciclo interno) n: cantidad de ciudades o nodos
            o(n) la comparacion de (for i in range(matriz.shape[0])) 
   
   
   '''
   intentos = 10  # Número de intentos antes de rendirse
   while intentos > 0: #o(1), se ejecuta max 10 veces y todo lo que esta dentro del ciclo es #o(1)
      nodo_0 = random.randint(0, matriz.shape[0]-1)  
      nodos_visitados = [nodo_0] 
      costo_viaje = 0 
      camino_valido = True

      while len(nodos_visitados) < matriz.shape[0]: #o(n: cantidad de ciudades)
         min = (float('inf'), float('inf'))  # nodo más cercano, distancia

         for i in range(matriz.shape[0]): #o(v: cantidad de ciudades visitadas, a lo sumo son todas!! esta acotado)
            dist_actual = matriz[nodo_0][i]
            if (dist_actual < min[1]) and (i not in nodos_visitados) and (dist_actual != 0): 
               min = (i, dist_actual)

         if min[0] == float('inf'):
            camino_valido = False
            break
         
         #Se agrega al nodo mas cercano, y se actualiza el costo
         nodos_visitados.append(min[0])
         nodo_0 = min[0]
         costo_viaje += min[1]

      #Se construyo un camino valido
      if camino_valido:
         # Agregar la última ciudad que es la misma que la primera y el costo de la anteúltima a la primera
         nodos_visitados.append(nodos_visitados[0])
         valor = matriz[nodos_visitados[-2]][nodos_visitados[0]]
         costo_viaje += valor
         return nodos_visitados, costo_viaje
        
      else:
         print("Error: No se construyó un camino válido. Intentando de nuevo...")
         intentos -= 1

   print("Error: No se pudo encontrar un camino válido después de varios intentos.")
   return None, float('inf')

'''
nodos_visitados, costo_viaje=vecino_mas_cercano(grafo)
print("Con la heuristica golosa estos son los nodos visitados y el costo: ")
print(nodos_visitados, costo_viaje)
print("______________________")
'''
# HEURISTICA 2: algoritmo goloso: vecino mas cercano de todos los que componen el camino
def vecino_mas_cercano_de_todos(matriz):
   n=matriz.shape[0]
   nodo_0 = random.randint(0, n-1)
   nodo_1 = random.randint(0, n-1)
   
   while nodo_1 == nodo_0 or matriz[nodo_0][nodo_1] == 0 or matriz[nodo_1][nodo_0]==0:
        nodo_1 = random.randint(0, n-1)
        
   
   nodos_visitados = [nodo_0,nodo_1,nodo_0]
   costo_viaje = matriz[nodo_0][nodo_1] + matriz[nodo_1][nodo_0]

   nodos_no_visitados = [i for i in range(matriz.shape[0]) if i not in nodos_visitados]
   while len(nodos_visitados) < n+1:
      min = (float('inf'), None)  # distancia, (la ciudad, la ciudad y la nueva proxima ciudad)
      
      for i in range(len(nodos_visitados)-1): #o(v) , no considero cambiar la primer ciudad que esta ubicada al final
         for j in nodos_no_visitados:
            pri_ciudad=nodos_visitados[i]
            seg_ciudad = nodos_visitados[i + 1]
            
            if (matriz[pri_ciudad][j] != 0 and matriz[j][seg_ciudad] != 0):
               posible_costo=costo_viaje+matriz[pri_ciudad][j] + matriz[j][seg_ciudad]-matriz[pri_ciudad][seg_ciudad]

               if( posible_costo<min[0]):
                  min = (posible_costo, (pri_ciudad,j))
   
      #Hago el cambio si hay una tupla valida
      if(min[0]!=float('inf')):
         ciudades=min[1]
         pri_ciudad=ciudades[0]
         nueva_ciudad=ciudades[1]
         seg_ciudad=nodos_visitados[nodos_visitados.index(pri_ciudad)+1]

         costo_viaje-=matriz[pri_ciudad][seg_ciudad]
         costo_viaje+=matriz[pri_ciudad][nueva_ciudad] +matriz[nueva_ciudad][seg_ciudad]
         
         nodos_visitados.insert(nodos_visitados.index(pri_ciudad)+1, nueva_ciudad)
         nodos_no_visitados.remove(nueva_ciudad)

      
      else: 
            print("Error: No se pudo construir un camino válido.")
            return None, float('inf')
      
   return nodos_visitados,costo_viaje
'''
camino, costo = vecino_mas_cercano_de_todos(grafo)
print(camino,costo)

'''
#########################Operadores de busqueda local
#############Relocate
def es_posible_relocate(i, j, recorrido, matriz):
    # Verificar que la nueva posición no genere un recorrido inválido
    if i < j:
        if 0 != matriz[recorrido[i-1]][recorrido[i+1]] and 0 != matriz[recorrido[j]][recorrido[i]] and 0 != matriz[recorrido[i]][recorrido[j+1]]:
            return True
    elif i > j:
        if 0 != matriz[recorrido[i-1]][recorrido[i+1]] and 0 != matriz[recorrido[j-1]][recorrido[i]] and 0 != matriz[recorrido[i]][recorrido[j]]:
            return True
    return False

def bl_relocate(recorrido, costo_viaje, matriz):
    mejor = (recorrido, costo_viaje)
    n = len(recorrido)
    
    for i in range(1, n-1): # La primer ciudad no se mueve y la última tampoco
        for j in range(1, n-1): 
            if i != j and es_posible_relocate(i, j, recorrido, matriz):
                posible_recorrido = recorrido.copy()
                
                if i < j:
                    ciudad = posible_recorrido.pop(i)
                    posible_recorrido.insert(j, ciudad)
                else:
                    ciudad = posible_recorrido.pop(i)
                    posible_recorrido.insert(j, ciudad)
                
                costo_viaje_nuevo = 0
                for k in range(n-1):
                    costo_viaje_nuevo += matriz[posible_recorrido[k]][posible_recorrido[k+1]]
                
                if costo_viaje_nuevo < mejor[1]:
                    mejor = (posible_recorrido, costo_viaje_nuevo)
    
    return mejor
camino, costo = vecino_mas_cercano_de_todos(grafo)
print(camino, costo)
print('////////////')
print(bl_relocate(camino, costo,grafo))


#############Swap

def es_posible(i,j, recorrido, matriz):
      if(abs(i-j)==1 and 0!=matriz[recorrido[i-1]][recorrido[j]] and 0!=matriz[recorrido[i]][recorrido[j+1]]):
            return True
         
      if(0!=matriz[recorrido[i-1]][recorrido[j]] and 0!=matriz[recorrido[j]][recorrido[i+1]] and  0!=matriz[recorrido[j-1]][recorrido[i]] and 0!=matriz[recorrido[i]][recorrido[j+1]]):
         return True
      
      else:
         return False
   
def bl_swap(recorrido, costo_viaje, matriz):
   mejor=(recorrido,costo_viaje)
   n = len(recorrido)

   for i in range(1,n-2): #La primer ciudad no se swapea y la ultima tampoco
      for j in range(i+1,n-1): 
         costo_viaje_viejos=costo_viaje
         if(es_posible(i,j,recorrido,matriz)):
            posible_recorrido=recorrido.copy()
            if(abs(i-j)==1): #Caso donde i e j son contiguos. 
               costo_viaje_viejos=costo_viaje_viejos-matriz[posible_recorrido[i-1]][posible_recorrido[i]]-matriz[posible_recorrido[j]][posible_recorrido[j+1]]- matriz[posible_recorrido[i]][posible_recorrido[i+1]]
               posible_recorrido[i], posible_recorrido[j] = posible_recorrido[j], posible_recorrido[i]
               costo_viaje_nuevo = costo_viaje_viejos+ matriz[posible_recorrido[i-1]][posible_recorrido[i]]+ matriz[posible_recorrido[i]][posible_recorrido[i+1]]+ matriz[posible_recorrido[j]][posible_recorrido[j+1]]

            # Resta los costos de los caminos viejos
            else:
               costo_viaje_viejos=costo_viaje_viejos-matriz[posible_recorrido[i-1]][posible_recorrido[i]]- matriz[posible_recorrido[i]][posible_recorrido[i+1]]-matriz[posible_recorrido[j-1]][posible_recorrido[j]]-matriz[posible_recorrido[j]][posible_recorrido[j+1]]
                
               # Intercambiar los elementos
               posible_recorrido[i], posible_recorrido[j] = posible_recorrido[j], posible_recorrido[i]
                
               # Sumar los costos de los nuevos caminos
               costo_viaje_nuevo = costo_viaje_viejos+ matriz[posible_recorrido[i-1]][posible_recorrido[i]]+ matriz[posible_recorrido[i]][posible_recorrido[i+1]]+matriz[posible_recorrido[j-1]][posible_recorrido[j]]+ matriz[posible_recorrido[j]][posible_recorrido[j+1]]

            # Actualizar el mejor resultado si el nuevo costo es menor
            if(costo_viaje_nuevo<mejor[1]):
               mejor=(posible_recorrido,costo_viaje_nuevo)
   
   
   return mejor

def recorrer_vecindarios(recorrido, costo_viaje, matriz):
    mejor = (recorrido, costo_viaje)
    while True:
        nuevo_mejor = bl_swap(mejor[0], mejor[1], matriz)
        if nuevo_mejor[1] >= mejor[1]:  # No hubo mejora
            break
        mejor = nuevo_mejor
    return mejor
   
'''
print(recorrer_vecindarios(nodos_visitados, costo_viaje,grafo))
'''