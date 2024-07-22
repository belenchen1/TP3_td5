def encontrar_ciudad_faltante(recorrido, total_ciudades):
    todas_las_ciudades = set(range(total_ciudades))
    ciudades_visitadas = set(recorrido)
    ciudad_faltante = todas_las_ciudades - ciudades_visitadas
    return ciudad_faltante

recorrido = [14, 3, 5, 4, 6, 0, 1, 2, 9, 11, 10, 13, 12, 7, 15, 8]
total_ciudades = 16
ciudad_faltante = encontrar_ciudad_faltante(recorrido, total_ciudades)

print("Ciudad faltante:", ciudad_faltante)
