import pulp 
'''
4 variaveis, uma para cada restrição

1. sum(k) (xi_k) ≤ fmaxj (somatorio das crianças k que recebem o presente i ≤ fmaxi)
i fixo; k a variar;

2. sum(i) (xk_i) ≤ 1 (somatorio dos presentes i que a criança k recebe ≤ 1)
k fixo; i a variar;

3. sum(k) (xj_k) ≥ pminj (somatorio das crianças k que recebem presente e pertencem ao pais j ≥ pminj)
j fixo; k a variar

4. sum(j) (xp_j) ≤ pmaxp (somatorio dos paises j que receberam brinquedos do pais p)
p fixo; j a variar;

5. sum(i) (xk_i) ≤ 0 (somatorio dos i brinquedos nao pertencentes aos wishes(k))
k fixo; i varia dentro dos wishes

Função objetivo 

xi_k = 1 se a criança k recebe o presente i, 0 caso contrario

maximizar: 
sum (xi_k) (somatorio das crianças k que recebem o presente i)
i e j a variar
'''

#leitura do input 
input_list = input().split(" ")
n_factories = int(input_list[0])
m_countries = int(input_list[1])
t_kids = int(input_list[2])

factories_info = tuple()
countries_info = tuple()
kids_info = tuple()


for i in range(n_factories):
    input_list = input().split(" ")
    factories_info += (int(input_list[1]),) # country
    factories_info += (int(input_list[2]),) # maximum


for j in range(m_countries):
    input_list = input().split(" ")
    countries_info += (int(input_list[1]),) # minimum
    countries_info += (int(input_list[2]),) # maximum

for t in range(t_kids):
    input_list = input().split(" ")
    aux = list()
    for element in input_list:
        aux.append(int(element))
    kids_info += (aux[1],) # country
    kids_info += (aux[2:],) # wishes


#Dar print para verificar se o input foi captado corretamente
# print("Número de fábricas: " + str(n_factories) + ".")
# print("Números de países: " + str(m_countries) + ".")
# print("Número de crianças: " + str(t_kids) + ".")
# print("Lista com os índices dos países que pertence a fábrica i: " + str(factory_country) + ".")
# print( "Lista com a produção máxima da fábrica i " + str(factories_maximum) + ".")
# print("Lista com a exportação máxima do país j: " + str(countries_maximum) + ".")
# print("Lista com a exportação mínima do país j: " + str(countries_minimum) + ".")
# print("Lista com os países em que a criança k vive: " + str(kids_countries) + ".")
# print("Lista com listas onde o brinquedo que a criança k quer é produzido: " + str(kids_wishes) + ".")

#Definir o porblema de programação linear
problem = pulp.LpProblem("projeto3", pulp.LpMaximize)

#Captar os nomes das variáveis
x_k_i_names = ["x_" + str(k+1)  + "_" + str(i+1) for k in range(t_kids) for i in range(n_factories)]

'''
1. sum(k) (xi_k) ≤ fmaxj (somatorio das crianças k que recebem o presente i ≤ fmaxi)
i fixo; k a variar;
2. sum(i) (xk_i) ≤ 1 (somatorio dos presentes i que a criança k recebe ≤ 1)
k fixo; i a variar;
3. sum(k) (xj_k) ≥ pminj (somatorio das crianças k que recebem presente e que pertencem ao pais j ≥ pminj)
j fixo; k a variar
4. sum(j) (xp_j) ≤ pmaxp (somatorio dos paises j que receberam brinquedos do pais p)
p fixo; j a variar;
'''


# nota que faço distincao entre xi_k (k varia) e xk_i (i varia): 
# xi_k = 1 significa que a criança k recebe i; uma outra criança k2 tambem pode receber i 
# xk_i = 1 signfica que a criança k recebe i; no entanto, temos de garantir que para qualquer outro i2, xk_i2 = 0 (nao pode receber mais que um presente) 

#Definir as variáveis do problema

x_k_i_vars = pulp.LpVariable.dict("", x_k_i_names, 0, 1, pulp.LpInteger)
# x_k_i = 1 se a crianca k recebe o brinquedo i


#definir o Objetivo (podemos escolher o xi_k ou xk_i)

problem += (pulp.lpSum([x_k_i_vars[c] for c in x_k_i_names]), "Objectivo")

#Restrições ao problema
'''
1. sum(k) (xi_k) ≤ fmaxj (somatorio das crianças k que recebem o presente i ≤ fmaxi)
i fixo; k a variar;
'''

for i in range(0, 2*n_factories, 2):
    
    criancas_recebem_i = []
    for k in range(t_kids):
        criancas_recebem_i.append(x_k_i_vars[f"x_{k+1}_{(i//2)+1}"])

    problem += (pulp.lpSum(criancas_recebem_i) <= factories_info[i+1], f"restricao1_{(i//2)+1}")
    del criancas_recebem_i

'''
2. sum(i) (xk_i) ≤ 1 (somatorio dos presentes i que a criança k recebe ≤ 1)
k fixo; i a variar;
'''
for k in range(0, 2*t_kids, 2):
    
    crianca_recebe = []
    for i in range(n_factories):
        crianca_recebe.append(x_k_i_vars[f"x_{(k//2)+1}_{i+1}"])
    
    problem += (pulp.lpSum(crianca_recebe) <= 1, f"restricao2_{(k//2)+1}")
    del crianca_recebe

'''
3. sum(k) (xj_k) ≥ pminj (somatorio das crianças k que recebem presente e que pertencem ao pais j ≥ pminj)
j fixo; k a variar
passa a - sum(k) (xj_k) ≤ -pminj
'''

for j in range(0, 2*m_countries, 2):
    
    criancas_de_j = []
    for k in range(0, t_kids*2, 2):
        if kids_info[k] == (j//2)+1:
            criancas_de_j.append((k//2)+1)

    crianca_de_j_recebe = []
    for crianca in criancas_de_j:
        for i in range(n_factories):
            crianca_de_j_recebe.append(x_k_i_vars[f"x_{crianca}_{(i//2)+1}"])
            
    del criancas_de_j
    problem += ((pulp.lpSum(crianca_de_j_recebe)) >= countries_info[j], f"restricao3_{(j//2)+1}")
    del crianca_de_j_recebe

'''
4. sum(j) (xp_j) ≤ pmaxp (somatorio dos paises j que receberam brinquedos do pais p)
p fixo; j a variar;
'''
for p in range(0, 2*m_countries, 2):

    brinquedos_de_p = []
    for i in range(0, 2*n_factories, 2):
        if factories_info[i] == (p//2)+1:
            brinquedos_de_p.append((i//2)+1)

    criancas_estrangeiras = []
    for k in range(0, 2*t_kids, 2):
        if kids_info[k] != (p//2)+1:
            criancas_estrangeiras.append((k//2)+1)
    
    exportacoes_de_p = []
    for crianca in criancas_estrangeiras:
        for brinquedo in brinquedos_de_p:
            exportacoes_de_p.append(x_k_i_vars[f"x_{crianca}_{brinquedo}"])
    
    del brinquedos_de_p
    del criancas_estrangeiras
    problem += ((pulp.lpSum(exportacoes_de_p)) <= countries_info[p+1], f"restricao4_{(p//2)+1}")
    del exportacoes_de_p


'''
5. sum(i) (xk_i) ≤ 0 (somatorio dos i brinquedos nao pertencentes aos wishes(k))
k fixo; i varia dentro dos wishes
'''

for k in range(0, 2*t_kids, 2):

    not_wished = []
    for i in range(0, 2*n_factories, 2):
        if ((i//2)+1 not in kids_info[k+1]):
            not_wished.append((i//2)+1)
    
    not_wished_but_received = []

    for b in not_wished:
        not_wished_but_received.append(x_k_i_vars[f"x_{(k//2)+1}_{b}"])

    del not_wished
    problem += ((pulp.lpSum(not_wished_but_received)) <= 0, f"restricao5_{(k//2)+1}")
    del not_wished_but_received


del input_list 

del factories_info
del countries_info
del kids_info


problem.solve(pulp.GLPK(msg=0))

if (problem.status == -1) :
    print (-1)
else:
    print (int(pulp.value(problem.objective)))

for v in x_k_i_vars:
    print (v)
    print(x_k_i_vars[v].varValue)