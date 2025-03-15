#include <iostream>
#include <vector>
#include <unordered_set>
#include <climits>

struct Node {
    // usados na criação do grafo reduzido
    std::unordered_set<int> adjacents; // linhas adjacentes no grafo reduzido
    bool created = false;
    int line_id; // id da linha no grafo reduzido

    // usados na BFS
    int distance;
    bool visited; 
};

int apply_bfs(std::vector<Node> nodes, int num_lines, int line, int *connectivity) {
    

    for (int i = 0; i < num_lines; i++) {
        nodes[i].distance = INT_MAX; // infinito
        nodes[i].visited = 0;
    }

    nodes[line].distance = 0;
    nodes[line].visited = 1;

    std::vector<Node*> queue;
    queue.push_back(&nodes[line]);

    int max_distance = 0;

    while (!queue.empty()) {
        Node *current = queue[0];
        queue.erase(queue.begin());
        for (int adj : current->adjacents) {
            if (!nodes[adj].visited) {
                nodes[adj].distance = current->distance + 1;
                nodes[adj].visited = true;
                queue.push_back(&nodes[adj]);

                if (nodes[adj].distance > max_distance) {
                    max_distance = nodes[adj].distance;
                }
            }
        }
    }

    // ver se algum nó não é alcançável
    for (int i = 0; i < num_lines; i++) {
        if (nodes[i].distance == INT_MAX) {
            *connectivity = -1;
            return 0;
        }
    }

    *connectivity = max_distance;

    return 0;

}

int main(){
    std::ios::sync_with_stdio(0);
    std::cin.tie(0);

    int num_stations, num_conections, num_lines;
    std::cin >> num_stations >> num_conections >> num_lines;

    // criar grafo, que tem num_lines; cada linha tem um conjunto de estações
    std::vector<std::unordered_set<int>> graph(num_lines);
    std::unordered_set<int> not_isolated_stations;
    bool no_changes_needed = false;

    for (int i = 0; i < num_conections; i++) {
        int v1, v2, line;
        std::cin >> v1 >> v2 >> line;
        graph[line-1].insert(v1);
        graph[line-1].insert(v2);
        not_isolated_stations.insert(v1);
        not_isolated_stations.insert(v2);

        // ver se é possivel chegar a todas as estações sem mudar de linha
        if ((int)graph[line-1].size() == num_stations) {
            no_changes_needed = true;
        }
    }
    if (no_changes_needed) {
        std::cout << "0" << std::endl;
        return 0;
    }

    // ver se alguma estacao esta isolada
    if ((int)not_isolated_stations.size() < num_stations) {
        std::cout << "-1" << std::endl;
        return 0;

    }

    // criar grafo onde os vértices são as linhas de metro e as arestas são as estações em comum
    std::vector<Node> nodes(num_lines);

    for (int i = 0; i < num_lines; i++) {

        if (!nodes[i].created) {
            Node node;
            node.line_id = i;
            node.created = true;
            nodes[i] = node;
        }

        for (int station : graph[i]) {
            for (int j = 0; j < num_lines; j++) {
                
                if (!nodes[j].created) {
                    Node node;
                    node.line_id = j;
                    node.created = true;
                    nodes[j] = node;
                }

                if (j == i) continue; 

                if (graph[j].find(station) != graph[j].end()) {
                    nodes[i].adjacents.insert(j);
                    nodes[j].adjacents.insert(i);
            }
        }
    }
}

    // ver se alguma linha está isolada
    for (int i = 0; i < num_lines; i++) {
        if (nodes[i].adjacents.size() == 0) {
            std::cout << "-1" << std::endl;
            return 0;
        }
    }

    // aplicar BFS para encontrar o menor caminho entre duas estações
    
    int metro_connectivity = 0;
    int connectivity = 0;

    for (int i = 0; i < num_lines; i++) {

            apply_bfs(nodes, num_lines, i, &connectivity);

            if (connectivity == -1) {
                std::cout << "-1" << std::endl;
                return 0;
            }
            if (connectivity > metro_connectivity) {
                metro_connectivity = connectivity;
            }
    }

    std::cout << metro_connectivity << std::endl;
    
    return 0;

}