from dataclasses import dataclass

@dataclass
class Cammino:
    id_connessione: int
    id_rifugio1: int
    id_rifugio2: int
    difficolta: int
    anno: int
    durata: int
    nome1: str
    localita1: str
    nome2: str
    localita2: str
    distanza: float

    def __hash__(self):
        return hash(self.id_connessione)