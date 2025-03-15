import pulp 
from sys import stdin
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
input_list = stdin.readline().rstrip('\n').split(" ")
n_factories = int(input_list[0])
m_countries = int(input_list[1])
t_kids = int(input_list[2])

factories = dict()
countries = dict()
kids = dict()

for i in range(n_factories):
    input_list = stdin.readline().rstrip('\n').split(" ")
    factories[int(input_list[0])] = [int(input_list[1]),int(input_list[2])]

for j in range(m_countries):
    input_list = stdin.readline().rstrip('\n').split(" ")
    countries[int(input_list[0])] = [int(input_list[1]),int(input_list[2])]

for t in range(t_kids):
    input_list = stdin.readline().rstrip('\n').split(" ")
    aux = list()
    for i in range(2, len(input_list)):
        if factories[int(input_list[i])][1]  > 0:
            aux.append(int(input_list[i]))
    kids[int(input_list[0])] = [int(input_list[1]), aux]



#Definir o porblema de programação linear
problem = pulp.LpProblem("Projeto3", pulp.LpMaximize)

#Captar os nomes das variáveis
x_k_i_names = ["x_" + str(k)  + "_" + str(i) 
            for k in range(1, t_kids +1) 
            for i in range(1, n_factories +1) 
            if (kids[k][1] != list() and i in kids[k][1] and factories[i][1] != 0)]

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

x_k_i_vars = pulp.LpVariable.dicts("", x_k_i_names, 0, 1, pulp.LpInteger)
# x_k_i = 1 se a crianca k recebe o brinquedo i


#definir o Objetivo (podemos escolher o xi_k ou xk_i)

problem += (pulp.lpSum([x_k_i_vars[a] for a in x_k_i_names]), "Objectivo")

#Restrições ao problema
    
'''
1. sum(k) (xi_k) ≤ fmaxj (somatorio das crianças k que recebem o presente i ≤ fmaxi)
i fixo; k a variar;
'''

for i in range(1, n_factories + 1):
    if( factories[i][1] == 0):
       continue
    problem += (pulp.lpSum(
        x_k_i_vars[f"x_{k}_{i}"] 
        for k in range (1, t_kids + 1) if (i in kids[k][1])) 
        <= factories[i][1], f"restricao1_{i}")
        
'''
2. sum(i) (xk_i) ≤ 1 (somatorio dos presentes i que a criança k recebe ≤ 1)
k fixo; i a variar;
'''
for k in range(1, t_kids + 1):
    if kids[k][1] == []:
        continue
    problem += (pulp.lpSum(
        x_k_i_vars[f"x_{k}_{i}"] 
        for i in  kids[k][1]) 
        <= 1, f"restricao2_wished_{k}")

'''
3. sum(k) (xj_k) ≥ pminj (somatorio das crianças k que recebem presente e que pertencem ao pais j ≥ pminj)
j fixo; k a variar
sum(k) (xj_k) ≥ pminj
'''

for j in range(1, m_countries + 1):
    
    problem += (pulp.lpSum(
        x_k_i_vars[f"x_{k}_{i}"] 
        for k in range (1, t_kids + 1) if kids[k][0] == j
        for i in range (1, n_factories + 1) if (i in kids[k][1]))
        
        >= countries[j][1], f"restricao3_{j}")
    
    problem += (pulp.lpSum(
        x_k_i_vars[f"x_{k}_{i}"] 
        for k in range(1, t_kids + 1) if kids[k][0] != j
        for i in range(1, n_factories +1) if (factories[i][0] ==j and i in kids[k][1]))

        <= countries[j][0], f"restricao4_{j}")
    
    

problem.solve(pulp.GLPK(msg=0))

if (problem.status == -1) :
    print (-1)
else:
    print (int(pulp.value(problem.objective)))

# for v in x_k_i_vars:
#     print (v)
#     print(x_k_i_vars[v].varValue)