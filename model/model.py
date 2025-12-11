import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self.nodes = None
        self.edges = None
        self.fattori= {"facile":1, "media":1.5, "difficile": 2}
        # Dizionario che mappa: id_rifugio → oggetto Rifugio
        self.rifugi = {
            r.id: r
            for r in DAO.get_all_rifugi() }

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        self.G.clear()
        self.edges= DAO.get_all_cammini()
        for edge in self.edges:
            if edge.anno <= year:
                fattore = self.fattori.get(edge.difficolta)
                peso= float(edge.distanza) * fattore
                self.G.add_edge(edge.id_rifugio1, edge.id_rifugio2, weight=peso,
                                localita1= edge.localita1, localita2= edge.localita2, nome1= edge.nome1, nome2= edge.nome2)


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        #ci sarebbe un altro metodo utilizzando pesi = list(nx.get_edge_attributes(G, "weight").values())
        lista_pesi=[]
        edges= self.G.edges(data=True)
        for edge in edges:
            nodo1=edge[0]
            nodo2=edge[1]
            data= edge[2]
            peso= data["weight"]
            lista_pesi.append(peso)
        peso_min= min(lista_pesi)
        peso_max= max(lista_pesi)
        return peso_min, peso_max

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        edges = self.G.edges(data=True)
        num_edges_peso_min=0
        num_edges_peso_mag=0
        for edge in edges:
            nodo1 = edge[0]
            nodo2 = edge[1]
            data = edge[2]
            peso = data["weight"]
            if peso < soglia:
                num_edges_peso_min += 1
            elif peso > soglia:
                num_edges_peso_mag += 1
        return num_edges_peso_min, num_edges_peso_mag

    """Implementare la parte di ricerca del cammino minimo"""

    def cerca_cammino_minimo(self, soglia):

        # costruisco un sottografo con archi > soglia
        H = nx.Graph()
        for u, v, d in self.G.edges(data=True):
            if d["weight"] > soglia:
                H.add_edge(u, v, weight=d["weight"])

        # variabili globali della ricerca
        self.best_path = []
        self.best_weight = float("inf")

        # avvio DFS da ciascun nodo
        for start in H.nodes():
            self._dfs(H, start, [start], 0.0)

        if self.best_path == []:
            return [], None

        return self.best_path, self.best_weight

    def _dfs(self, H, current, parziale, peso_parziale):
        """
        DFS semplice:
        - H = sottografo
        - current = ultimo nodo aggiunto
        - parziale = cammino corrente
        - peso_parziale = somma pesi attuale
        """

        # Se il cammino contiene almeno 3 nodi il candidato è valido
        if len(parziale) >= 3:
            if peso_parziale < self.best_weight:
                self.best_weight = peso_parziale
                self.best_path = parziale.copy()

        # continuo ad esplorare
        for vicino in H.neighbors(current):
            if vicino in parziale:
                continue  # niente cicli

            w = H[current][vicino]["weight"]

            # espando il cammino
            parziale.append(vicino)
            self._dfs(H, vicino, parziale, peso_parziale + w)

            # backtracking
            parziale.pop()

