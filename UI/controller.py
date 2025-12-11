import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        """Callback per il pulsante 'Crea Grafo'."""
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi")
        )
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()

    def handle_conta_archi(self, e):
        """Callback per il pulsante 'Conta Archi'."""
        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Archi < {soglia}: {minori}, Archi > {soglia}: {maggiori}"))
        self._view.page.update()

    """Implementare la parte di ricerca del cammino minimo"""

    def handle_cammino_minimo(self, e):
        """Callback per 'Cammino minimo'."""
        # 1) Leggo la soglia dalla view
        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        # 2) Chiamo il modello
        path, weight = self._model.cerca_cammino_minimo(soglia)

        # 3) Nessun cammino trovato → alert
        if path == []:
            self._view.show_alert("Nessun cammino trovato con archi > soglia.")
            return
        # 4) Mostro il risultato nella terza lista
        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(
            ft.Text("Cammino minimo:")
        )

        # --- STAMPA IN FORMA 'A TRATTI' ---
        output = ""
        for i in range(len(path) - 1):
            id1 = path[i]
            id2 = path[i+1]

            r1 = self._model.rifugi[id1]
            r2 = self._model.rifugi[id2]

            # recupero il peso dell'arco dal grafo
            peso_tratto = self._model.G[id1][id2]["weight"]

            output += (
                f"[{r1.id}] {r1.nome} ({r1.localita})  --  "
                f"[{r2.id}] {r2.nome} ({r2.localita})  --  "
                f"peso: [{peso_tratto:.2f}]\n")
        # stampo in Flet
        self._view.lista_visualizzazione_3.controls.append(ft.Text(output))
        self._view.page.update()
