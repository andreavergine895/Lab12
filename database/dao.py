from database.DB_connect import DBConnect
from model.cammini import Cammino
from model.rifugio import Rifugio
from model.connessione import Connessione

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def get_all_rifugi():
        conn= DBConnect.get_connection()
        risultati=[]
        cursor = conn.cursor(dictionary=True)
        query = "select * from rifugio"
        cursor.execute(query)
        for row in cursor:
            risultati.append(Rifugio(**row))
        return risultati



    @staticmethod
    def get_all_connessioni():
        conn= DBConnect.get_connection()
        risultati=[]
        cursor = conn.cursor(dictionary=True)
        query = "select * from connessione"
        cursor.execute(query)
        for row in cursor:
            risultati.append(Connessione(**row))
        return risultati


    @staticmethod
    def get_all_cammini():
        conn= DBConnect.get_connection()
        risultati=[]
        cursor = conn.cursor(dictionary=True)
        query = ('''select C.id as id_connessione, C.id_rifugio1, C.id_rifugio2, C.difficolta, C.anno, C.durata,
                    C.distanza, R1.nome as nome1, R1.localita as localita1, R2.nome as nome2, R2.localita as localita2
                    from connessione C, rifugio R1, rifugio R2
                    where C.id_rifugio1 = R1.id and C.id_rifugio2 = R2.id''')
        cursor.execute(query)
        for row in cursor:
            risultati.append(Cammino(**row))
        return risultati