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

    # --- Novos métodos ---
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

    # --- Novos métodos ---
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


if __name__ == "__main__":
    vertices_labels = ['A', 'B', 'C', 'D', 'E']
    g = GrafoEsparso(labels=vertices_labels)

    g.adicionar_aresta('A', 'B')
    g.adicionar_aresta('A', 'C')
    g.adicionar_aresta('C', 'D')
    g.adicionar_aresta('C', 'E')
    g.adicionar_aresta('B', 'D')

    g.imprimir()
    print(f"Número de vértices: {g.numero_de_vertices()}")
    print(f"Número de arestas: {g.numero_de_arestas()}")
    print(f"Sequência de graus: {g.sequencia_de_graus()}")
    print("É simples?", g.is_simples())
    print("É nulo?", g.is_nulo())
    print("É completo?", g.is_completo())
