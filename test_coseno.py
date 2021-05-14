usuarios = [[1,2,3],[4,5,3],[1,5,4],[3,4,4],[5,5,1]]

#variables para usar
numerador = 0
denominador_1 = 0
denominador_2 = 0

#datos formateados (se podrian combinar ambos bucles)
for i in usuarios:
    numerador += (i[0]-i[2])*(i[1]-i[2])
    denominador_1 += (i[0]-i[2])**2
    denominador_2 += (i[1]-i[2])**2

coseno_ajustado = numerador/((denominador_1**(1/2))*(denominador_2**(1/2)))
print(coseno_ajustado)