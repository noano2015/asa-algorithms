import pulp 

#leitura do input 
input_list = input().split(" ")
n_factories = int(input_list[0])
m_countries = int(input_list[1])
t_kids = int(input_list[2])

factories_info = [None] * (n_factories + 1) # country, max
countries_info = [None] * (m_countries + 1) # maximum, minimum
kids_info = [None] * (t_kids + 1)



for i in range(1, n_factories + 1):
    input_list = input().split(" ")
    factories_info[i] = [int(input_list[1]),int(input_list[2])]


for j in range(1, m_countries +1):
    input_list = input().split(" ")
    countries_info[j] = [int(input_list[1]),int(input_list[2])]

for t in range(1, t_kids +1):
    input_list = input().split(" ")
    aux = list()
    for element in input_list:
        aux.append(int(element))
    kids_info[t] = [aux[1], aux[2:]]


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
problem = pulp.LpProblem("Projeto3", pulp.LpMaximize)

#Captar os nomes das variáveis
x_k_i_names = ["x_" + str(k+1)  + "_" + str(i+1) for k in range(t_kids) for i in range(n_factories)]

# nota que faço distincao entre xi_k (k varia) e xk_i (i varia): 
# xi_k = 1 significa que a criança k recebe i; uma outra criança k2 tambem pode receber i 
# xk_i = 1 signfica que a criança k recebe i; no entanto, temos de garantir que para qualquer outro i2, xk_i2 = 0 (nao pode receber mais que um presente) 

#Definir as variáveis do problema

x_k_i_vars = pulp.LpVariable.dict("", x_k_i_names, 0, 1, pulp.LpInteger)
# x_k_i = 1 se a crianca k recebe o brinquedo i


#definir o Objetivo (podemos escolher o xi_k ou xk_i)

problem += (pulp.lpSum([x_k_i_vars[c] for c in x_k_i_names]), "Objectivo")

#Restrições ao problema

for i in range(1, n_factories + 1):

    problem += (pulp.lpSum(x_k_i_vars[f"x_{k}_{i}"] for k in range (1, t_kids + 1))  <= factories_info[i][1], f"restricao1_{i}")

for k in range(1, t_kids + 1):

    wished_sum = pulp.lpSum(
        x_k_i_vars[f"x_{k}_{i}"] 
        for i in kids_info[k][1])
    
    for i in range(1, n_factories +1):
        if i not in kids_info[k][1]:
            problem += (x_k_i_vars[f"x_{k}_{i}"] == 0, f"restricao2_not_wished_{k}_{i}")
    
    
    problem += (wished_sum <=1, f"restricao2.1_{k}")


for j in range(1, m_countries + 1):      
    
    problem += (pulp.lpSum(x_k_i_vars[f"x_{k}_{i}"] for k in range (1, t_kids + 1) if kids_info[k][0] == j
                        for i in range (1, n_factories + 1) )
                >= countries_info[j][1], f"restricao3_{j}")
    

for p in range(1, m_countries + 1):

    problem += (pulp.lpSum(
        x_k_i_vars[f"x_{k}_{i}"] 
        for i in range(1, n_factories + 1) if factories_info[i][0]== p
        for k in range(1, t_kids + 1) if kids_info[k][0] != p)
                <= countries_info[p][0], f"restricao4_{p}")
    


problem.solve(pulp.GLPK(msg=0))

if (problem.status == -1) :
    print (-1)
else:
    print (int(pulp.value(problem.objective)))

#for v in x_k_i_vars:
#    print (v)
#    print(x_k_i_vars[v].varValue)


#print("Factories Info:", factories_info)
#print("Countries Info:", countries_info)
#print("Kids Info:", kids_info)
