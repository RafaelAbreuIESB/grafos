import sys
from abc import ABC, abstractmethod

class Grafo(ABC):
    @abstractmethod
    def numero_de_vertices(self):
        pass

    @abstractmethod
    def numero_de_arestas(self):
        pass

    @abstractmethod
    def sequencia_de_graus(self):
        pass

    @abstractmethod
    def adicionar_aresta(self, u, v):
        pass

    @abstractmethod
    def remover_aresta(self, u, v):
        pass

    @abstractmethod
    def imprimir(self):
        pass

    @abstractmethod
    def get_vertices(self):
        pass

    @abstractmethod
    def get_arestas(self):
        pass

    @abstractmethod
    def is_subgrafo(self, outro_grafo):
        pass

    @abstractmethod
    def is_subgrafo_gerador(self, outro_grafo):
        pass

    @abstractmethod
    def is_subgrafo_induzido(self, outro_grafo):
        pass


# ============================================================
# GRAFO DENSO (Matriz de adjacência)
# ============================================================
class GrafoDenso(Grafo):
    def __init__(self, num_vertices=None, labels=None):
        if labels:
            self.labels = labels
            self.num_vertices = len(labels)
            self.mapa_labels = {label: i for i, label in enumerate(labels)}
        elif num_vertices:
            self.num_vertices = num_vertices
            self.labels = [str(i) for i in range(num_vertices)]
            self.mapa_labels = {str(i): i for i in range(num_vertices)}
        else:
            print("Erro: Forneça 'num_vertices' ou uma lista de 'labels'.")
            sys.exit(1)

        self.matriz = [[0] * self.num_vertices for i in range(self.num_vertices)]
        
    def numero_de_vertices(self):
        return self.num_vertices

    def numero_de_arestas(self):
        count = 0
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.matriz[i][j] != 0:
                    count += 1
        return count

    def sequencia_de_graus(self):
        return sorted([sum(row) for row in self.matriz])

    def _obter_indice(self, vertice):
        if isinstance(vertice, str) and vertice in self.mapa_labels:
            return self.mapa_labels[vertice]
        elif isinstance(vertice, int) and 0 <= vertice < self.num_vertices:
            return vertice
        else:
            raise ValueError(f"Vértice '{vertice}' é inválido.")

    def adicionar_aresta(self, u, v):
        try:
            idx_u = self._obter_indice(u)
            idx_v = self._obter_indice(v)
            self.matriz[idx_u][idx_v] += 1
            self.matriz[idx_v][idx_u] += 1
            print(f"Aresta adicionada entre {u} e {v}.")
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")

    def remover_aresta(self, u, v):
        try:
            idx_u = self._obter_indice(u)
            idx_v = self._obter_indice(v)
            if self.matriz[idx_u][idx_v] == 0:
                print(f"Aresta entre {u} e {v} não existe.")
                return
            self.matriz[idx_u][idx_v] -= 1
            self.matriz[idx_v][idx_u] -= 1
            print(f"Aresta removida entre {u} e {v}.")
        except ValueError as e:
            print(f"Erro ao remover aresta: {e}")

    def imprimir(self):
        print("\nMatriz de Adjacência:")
        header = "   " + "  ".join(self.labels)
        print(header)
        print("─" * len(header))
        for i, linha in enumerate(self.matriz):
            print(f"{self.labels[i]} |", "  ".join(map(str, linha)))
        print()

    # --- Atividade 1 ---
    def is_simples(self):
        for i in range(self.num_vertices):
            if self.matriz[i][i] != 0:  # laço
                return False
            for j in range(i + 1, self.num_vertices):
                if self.matriz[i][j] > 1:  # múltiplas arestas
                    return False
        return True

    def is_nulo(self):
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.matriz[i][j] != 0:
                    return False
        return True

    def is_completo(self):
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if i != j and self.matriz[i][j] == 0:
                    return False
        return True

    # --- Atividade 3 ---
    def get_vertices(self):
        return self.labels

    def get_arestas(self):
        arestas = []
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.matriz[i][j] > 0:
                    arestas.append((self.labels[i], self.labels[j]))
        return arestas

    def is_subgrafo(self, outro_grafo):
        if not set(self.labels).issubset(set(outro_grafo.get_vertices())):
            return False
        if not set(self.get_arestas()).issubset(set(outro_grafo.get_arestas())):
            return False
        return True

    def is_subgrafo_gerador(self, outro_grafo):
        if set(self.labels) != set(outro_grafo.get_vertices()):
            return False
        return set(self.get_arestas()).issubset(set(outro_grafo.get_arestas()))

    def is_subgrafo_induzido(self, outro_grafo):
        if not set(self.labels).issubset(set(outro_grafo.get_vertices())):
            return False
        vertices = set(self.labels)
        for u in vertices:
            for v in vertices:
                if u != v and ((u, v) in outro_grafo.get_arestas() or (v, u) in outro_grafo.get_arestas()):
                    if (u, v) not in self.get_arestas() and (v, u) not in self.get_arestas():
                        return False
        return True


# ============================================================
# GRAFO ESPARSO (Lista de adjacência)
# ============================================================
class GrafoEsparso(Grafo):
    def __init__(self, num_vertices=None, labels=None):
        if labels:
            self.vertices = labels
        elif num_vertices:
            self.vertices = [str(i) for i in range(num_vertices)]
        else:
            print("Erro: Forneça 'num_vertices' ou uma lista de 'labels'.")
            sys.exit(1)

        self.lista_adj = {vertice: [] for vertice in self.vertices}

    def numero_de_vertices(self):
        return len(self.vertices)

    def numero_de_arestas(self):
        return int(sum([len(vizinhos) for vizinhos in self.lista_adj.values()])/2)

    def sequencia_de_graus(self):
        return sorted([len(values) for values in self.lista_adj.values()])

    def _validar_vertice(self, vertice):
        if vertice not in self.lista_adj:
            raise ValueError(f"Vértice '{vertice}' não existe no grafo.")
        return True

    def adicionar_aresta(self, u, v):
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)
            self.lista_adj[u].append(v)
            self.lista_adj[v].append(u)
            print(f"Aresta adicionada entre {u} e {v}")
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")

    def remover_aresta(self, u, v, peso=None):
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)

            for index, ver in enumerate(self.lista_adj[u]):
                if v == ver:
                    del self.lista_adj[u][index]
                    print(f"Aresta removida entre {u} e {v}.")
                    break
            else:
                print(f"Aresta entre {u} e {v} não existe.")

            for index, ver in enumerate(self.lista_adj[v]):
                if u == ver:
                    del self.lista_adj[v][index]
                    print(f"Aresta removida entre {v} e {u}.")
                    break
            else:
                print(f"Aresta entre {u} e {v} não existe.")

        except ValueError as e:
            print(f"Erro ao remover aresta: {e}")

    def imprimir(self):
        print("\nLista de Adjacências:")
        if not self.lista_adj:
            print("{}")
            return
        for vertice, vizinhos in self.lista_adj.items():
            saida = [vizinho for vizinho in vizinhos]             
            print(f"  {vertice} -> [ {saida} ]")
        print()

    # --- Atividade 1 ---
    def is_simples(self):
        for v, vizinhos in self.lista_adj.items():
            if v in vizinhos:  # laço
                return False
            if len(vizinhos) != len(set(vizinhos)):  # múltiplas arestas
                return False
        return True

    def is_nulo(self):
        for vizinhos in self.lista_adj.values():
            if vizinhos:
                return False
        return True

    def is_completo(self):
        n = len(self.vertices)
        for v, vizinhos in self.lista_adj.items():
            if len(set(vizinhos)) != n - 1:
                return False
        return True

    # --- Atividade 3 ---
    def get_vertices(self):
        return self.vertices

    def get_arestas(self):
        arestas = []
        for u, vizinhos in self.lista_adj.items():
            for v in vizinhos:
                if (v, u) not in arestas:  # evitar duplicação
                    arestas.append((u, v))
        return arestas

    def is_subgrafo(self, outro_grafo):
        if not set(self.vertices).issubset(set(outro_grafo.get_vertices())):
            return False
        if not set(self.get_arestas()).issubset(set(outro_grafo.get_arestas())):
            return False
        return True

    def is_subgrafo_gerador(self, outro_grafo):
        if set(self.vertices) != set(outro_grafo.get_vertices()):
            return False
        return set(self.get_arestas()).issubset(set(outro_grafo.get_arestas()))

    def is_subgrafo_induzido(self, outro_grafo):
        if not set(self.vertices).issubset(set(outro_grafo.get_vertices())):
            return False
        vertices = set(self.vertices)
        for u in vertices:
            for v in vertices:
                if u != v and ((u, v) in outro_grafo.get_arestas() or (v, u) in outro_grafo.get_arestas()):
                    if (u, v) not in self.get_arestas() and (v, u) not in self.get_arestas():
                        return False
        return True


# ============================================================
# Teste rápido
# ============================================================
if __name__ == "__main__":
    vertices_labels = ['A', 'B', 'C', 'D']
    g1 = GrafoEsparso(labels=vertices_labels)
    g1.adicionar_aresta('A', 'B')
    g1.adicionar_aresta('B', 'C')

    g2 = GrafoEsparso(labels=vertices_labels)
    g2.adicionar_aresta('A', 'B')
    g2.adicionar_aresta('B', 'C')
    g2.adicionar_aresta('C', 'D')
    g2.adicionar_aresta('A', 'D')

    print("\nG1:")
    g1.imprimir()
    print("G2:")
    g2.imprimir()

    print("\nSubgrafo?", g1.is_subgrafo(g2))
    print("Subgrafo gerador?", g1.is_subgrafo_gerador(g2))
    print("Subgrafo induzido?", g1.is_subgrafo_induzido(g2))
