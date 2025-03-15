#include <iostream>
#include <vector>
#include <climits>
#include <string>
#include <unordered_set>


/**
 * Cria os parentesis da solução mais à esquerda
 * 
 */
std::string create_parentesis( int i, int j, std::vector<int> &solution,
                            std::vector<std::vector<std::vector<std::vector<int>>>> &results,
                            std::vector<int> &sequence){
    
    if(i==j) return std::to_string(sequence[i]);
    
    std::vector<int> left_vec;
    for(std::vector<int> aux_left : results[i][solution[1]]){
        if(aux_left[0] == solution[2]){
            left_vec = aux_left;
            break;
        }
    }

    std::vector<int> right_vec;
    for(std::vector<int> aux_right : results[solution[1]+1][j]){
        if(aux_right[0] == solution[3]){
            right_vec = aux_right;
            break;
        }
    }

    return "(" + create_parentesis(i , solution[1], left_vec, results, sequence) +
            " " + create_parentesis(solution[1] + 1, j, right_vec, results, sequence) +
            ")";

}


int main(){
    std::ios::sync_with_stdio(0);
    std::cin.tie(0);
    
    int table_size, sequence_size;
    std::cin >> table_size >> sequence_size;

    //Lê a tabela com as operações entre os elementos da sequência
    std::vector<std::vector<int>> operations_table(table_size, std::vector<int>(table_size));
    for (int i = 0; i < table_size; i++) {
        for (int j = 0; j < table_size; j++) {
            std::cin >> operations_table[i][j];
        }
    }

    //Lê a sequência que pretende-se obter o resultado
    std::vector<int> sequence(sequence_size);
    for (int i = 0; i < sequence_size; i++) std::cin >> sequence[i]; 


    int target;
    std::cin >> target;

    //Uma matriz que guarda os valores que resultam das operações entre os valores da sequência
    std::vector<std::vector<std::vector<std::vector<int>>>> operation_results(sequence_size, 
                                                                std::vector<std::vector<std::vector<int>>>(sequence_size, 
                                                                std::vector<std::vector<int>>(0,
                                                                std::vector<int>(0))));
 
    
    //Prencher as diagonais com os valores da sequência
    for (int i = 0; i < sequence_size; i++) {
        std::vector<int> aux = {sequence[i]};
        operation_results[i][i].push_back(aux);
    }

    //Preencher as restantes entradas de ambas as matrizes em ordem 
    for (int diagonal = 1; diagonal < sequence_size; diagonal++) {

        for (int i = 0; i < sequence_size - diagonal; i++) {
            int j = i + diagonal;
            
            int contador = 0;
            std::vector<bool> existing_results(table_size, false);
            for (int k = j; k >= i; k--) {  // Separar o subarray em k

                if (contador == table_size) break;
                
                // Possiveis resultados do lado esquerdo 
                for (std::vector<int> left : operation_results[i][k]) {  

                    if (contador == table_size) break;

                    // Possiveis resultados do lado direito
                    for (std::vector<int> right : operation_results[k + 1][j]) { 

                        if (contador == table_size) break; 
                        
                        // Calcular o valor da operação entre os dois lados
                        int value = operations_table[left[0]-1][right[0]-1];

                        // Verificar se o valor já foi calculado
                        if(existing_results[value-1]) continue;

                        std::vector<int> aux = {value, k, left[0], right[0]};

                        // Adicionar o resultado da operação entre os dois lados
                        operation_results[i][j].push_back(aux); 

                        // Adicionar o valor à lista de resultados calculados
                        existing_results[value-1] = true;
                        contador++;

                        
                    }
                
                }
                
            }
        }
    }

    
    //Verificar se existe uma solução igual ao target
    bool solution = false;
    std::string parentesis;
    std::vector<std::vector<int>> aux = operation_results[0][sequence_size -1];
    for(size_t i = 0; i < aux.size(); i++){
        if(aux[i][0] == target){
            solution = true;
            parentesis = create_parentesis(0, sequence_size -1, aux[i], 
                                            operation_results, sequence);
            break;
        }
    }

    //Escrever o resultado final que se encontra na entrada da diagonal no canto superior direto
    if (solution) {
        std::cout << "1" << std::endl;
        std::cout << parentesis << std::endl;
    } else {
        std::cout << "0" << std::endl;
    }

    return 0;
}


