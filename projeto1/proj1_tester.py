import time
import subprocess
import random
import matplotlib.pyplot as plt
import numpy as np

# Caminho para o executável a ser testado
executavel = "proj1/main"

# Função para gerar o ficheiro de input
def gerar_input(n, m, nome_ficheiro="test.in"):
    with open(nome_ficheiro, "w") as ficheiro:
        ficheiro.write(f"{n} {m}\n")
        
        # Geração da matriz n x n
        for _ in range(n):
            linha = " ".join(str(random.randint(1, n)) for _ in range(n))
            ficheiro.write(linha + "\n")
        
        # Geração de m inteiros (expressao)
        ficheiro.write(" ".join(str(random.randint(1, n)) for _ in range(m)) + "\n")
        
        # Geração do resultado desejado
        ficheiro.write(str(random.randint(1, n)) + "\n")

# Função para medir o tempo de execução do programa com um dado input
def testar_velocidade(n, m):
    gerar_input(n, m)
    
    # Mede o tempo antes da execução
    inicio = time.time()
    
    # Executa o programa com o input do ficheiro
    with open("test.in", "r") as entrada:
        subprocess.run([executavel], stdin=entrada, stdout=subprocess.DEVNULL)
    
    # Mede o tempo após a execução
    fim = time.time()
    
    # Calcula o tempo total
    tempo_execucao = fim - inicio
    
    # Retorna o tempo
    return tempo_execucao

# Dicionários para guardar tempos de execução
tempos_n = {}
tempos_m = {}

# Testes variando n de 5 a 100 e m de 10 a 1000
for n in range(5, 101, 5):      # Incrementa n de 5 em 5 até 100
    tempos_n[n] = []
    for m in range(10, 1001, 25):  # Incrementa m de 50 em 50 até 1000
        tempo = testar_velocidade(n, m)
        tempos_n[n].append(tempo)
        
        # Guarda o tempo para m específico em todos os n
        if m not in tempos_m:
            tempos_m[m] = []
        tempos_m[m].append(tempo)
        
        print(f"n={n}, m={m} -> Tempo de execução: {tempo:.4f} segundos")

all_f_n_m_values = []
all_times = []

for n, tempos in tempos_n.items():
    m_values = list(range(10, 1001, 25))
    for i, m in enumerate(m_values):
        f_n_m = n * m
        all_f_n_m_values.append(f_n_m)
        all_times.append(tempos[i])

# Plota os pontos de dados originais
plt.scatter(all_f_n_m_values, all_times, label="Dados experimentais", alpha=0.5, color="blue")

# Ajusta uma curva polinomial de tendência para todos os dados combinados
degree = 2  # Ajusta o grau conforme necessário
coef = np.polyfit(all_f_n_m_values, all_times, degree)
poly_fn = np.poly1d(coef)

# Plota a curva de ajuste
sorted_nm_values = sorted(all_f_n_m_values)  # Ordena para uma curva suave
plt.plot(sorted_nm_values, poly_fn(sorted_nm_values), '--', label="Tendência global", color="red")

plt.xlabel("f(n, m) = n * m")
plt.ylabel("Tempo de execução (segundos)")
plt.title("Curva de tendência para tempo de execução em função de f(n, m)")
plt.legend()
plt.show()