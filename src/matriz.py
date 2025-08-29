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
    # Definição do grafo
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

        # Cria a matriz de adjacência NxN preenchida com zeros
        self.matriz = [[0] * self.num_vertices for i in range(self.num_vertices)]
        
    
    def numero_de_vertices(self):
        # Retorna o número total de vértices no grafo.
        return self.num_vertices

    def numero_de_arestas(self):
        # Retorna o número total de arestas no grafo.
        count = 0
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.matriz[i][j] != 0:
                    count += 1
        return count

    def sequencia_de_graus(self):
        # Retorna uma lista com os graus de todos os vértices.
        return sorted([sum(row) for row in self.matriz])


    def _obter_indice(self, vertice):
        if isinstance(vertice, str) and vertice in self.mapa_labels:
            return self.mapa_labels[vertice]
        elif isinstance(vertice, int) and 0 <= vertice < self.num_vertices:
            return vertice
        else:
            raise ValueError(f"Vértice '{vertice}' é inválido.")


    def adicionar_aresta(self, u, v):
        """
        Adiciona a aresta entre os vértices u e v.
        """
        try:
            idx_u = self._obter_indice(u)
            idx_v = self._obter_indice(v)

            self.matriz[idx_u][idx_v] = 1
            self.matriz[idx_v][idx_u] = 1

            print(f"Aresta adicionada entre {u} e {v}.")
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")


    def remover_aresta(self, u, v):
        """
        Remove a aresta entre os vértices u e v.
        """
        try:
            idx_u = self._obter_indice(u)
            idx_v = self._obter_indice(v)

            if self.matriz[idx_u][idx_v] == 0:
                print(f"Aresta entre {u} e {v} não existe.")
                return

            # Remove a aresta
            self.matriz[idx_u][idx_v] = 0
            self.matriz[idx_v][idx_u] = 0
            print(f"Aresta removida entre {u} e {v}.")
        
        except ValueError as e:
            print(f"Erro ao remover aresta: {e}")

    def imprimir(self):
        """Imprime a matriz de adjacência de forma legível."""
        print("\nMatriz de Adjacência:")
        # Imprime o cabeçalho das colunas
        header = "   " + "  ".join(self.labels)
        print(header)
        print("─" * len(header))

        # Imprime as linhas com seus respectivos rótulos
        for i, linha in enumerate(self.matriz):
            print(f"{self.labels[i]} |", "  ".join(map(str, linha)))
        print()


class GrafoEsparso(Grafo):
    """
    Implementa as operações básicas de um grafo não orientado
    usando uma LISTA DE ADJACÊNCIAS (implementada com um dicionário).
    """
    # (i) Definição do grafo
    def __init__(self, num_vertices=None, labels=None):

        if labels:
            self.vertices = labels
        elif num_vertices:
            self.vertices = [str(i) for i in range(num_vertices)]
        else:
            print("Erro: Forneça 'num_vertices' ou uma lista de 'labels'.")
            sys.exit(1)

        # A lista de adjacências é um dicionário onde cada vértice
        # é uma chave e o valor é a lista de seus vizinhos.
        self.lista_adj = {vertice: [] for vertice in self.vertices}

  
    def numero_de_vertices(self):
        # Retorna o número total de vértices no grafo.
        return len(self.vertices)

    def numero_de_arestas(self):
        # Retorna o número total de arestas no grafo.
        return int(sum([len(vizinhos) for vizinhos in self.lista_adj.values()])/2)


    def sequencia_de_graus(self):
        # Retorna uma lista com os graus de todos os vértices.
        return sorted([len(values) for values in self.lista_adj.values()])




    def _validar_vertice(self, vertice):
        """Método auxiliar para checar se um vértice existe no grafo."""
        if vertice not in self.lista_adj:
            raise ValueError(f"Vértice '{vertice}' não existe no grafo.")
        return True

    # (ii) Adição de arestas
    def adicionar_aresta(self, u, v):
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)

            # Pode adicionar aresta duplicada ou laço (loop)
            self.lista_adj[u].append(v)
            self.lista_adj[v].append(u)
 
            print(f"Aresta adicionada entre {u} e {v}")
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")


    # (v) Remoção de arestas
    def remover_aresta(self, u, v, peso=None):
        """
        Se existir mais de uma, remove a primeira aresta entre os vértices u e v.
        """
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
        """Imprime a lista de adjacências de forma legível."""
        print("\nLista de Adjacências:")
        if not self.lista_adj:
            print("{}")
            return
        for vertice, vizinhos in self.lista_adj.items():
            # Junta a lista de vizinhos em uma string para impressão
            saida = [vizinho for vizinho in vizinhos]             
            print(f"  {vertice} -> [ {saida} ]")
        print()



if __name__ == "__main__":
    
    vertices_labels = ['A', 'B', 'C', 'D', 'E']
    #g = GrafoDenso(labels=vertices_labels)
    g = GrafoEsparso(labels=vertices_labels)
  
    g.adicionar_aresta('A', 'B')
    g.adicionar_aresta('A', 'C')
    g.adicionar_aresta('A', 'C')
    g.adicionar_aresta('C', 'D')
    g.adicionar_aresta('C', 'E')
    g.adicionar_aresta('B', 'D')
    g.imprimir()
    print(f"Número de vértices: {g.numero_de_vertices()}")
    print(f"Número de arestas: {g.numero_de_arestas()}")
    print(f"Sequência de graus: {g.sequencia_de_graus()}")
    g.remover_aresta('A', 'C')
    g.imprimir()


    """"

    vertices_labels = ['A', 'B', 'C', 'D', 'E']
    g = GrafoDenso(labels=vertices_labels)

    print("Grafo inicial criado.")
    g.imprimir()

    # (ii) Adição de arestas
    print("\n--- Adicionando arestas ---")
    g.adicionar_aresta('A', 'B')
    g.adicionar_aresta('A', 'C')
    g.adicionar_aresta('B', 'A')
    g.adicionar_aresta('B', 'E')
    g.adicionar_aresta('C', 'A')
    g.imprimir()
    g.remover_aresta('A', 'C')
    g.imprimir()

    print(g.numero_de_arestas())
  

    g = GrafoDenso(num_vertices=5)
    print("Grafo inicial criado.")
    g.imprimir()
    g.adicionar_aresta(1, 2)
    g.adicionar_aresta(1, 3)
    g.adicionar_aresta(0, 4)
    g.adicionar_aresta(1, 4)
    g.adicionar_aresta(2, 3)
    g.imprimir()
    print(g.numero_de_vertices())
    print(g.numero_de_arestas())
    print(g.sequencia_de_graus())

"""
