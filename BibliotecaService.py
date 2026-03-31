from DBfunctions import DBFunctions
from datetime import date
from oggetti import Utente, Libro, NoleggioResponse, RestituisciResponse

class BibliotecaService:

    @staticmethod
    def get_libri():
        libri = DBFunctions.importa_catalogo()

        result = []
        for l in libri:
            result.append({
                "id": l[0],
                "titolo": l[1],
                "autore": l[2],
                "anno": l[3],
                "disponibile": bool(l[4])
            })

        return result
    
    @staticmethod
    def get_libri_noleggiati():
        libri_noleggiati = DBFunctions.importa_libri_noleggiati()

        result = []
        for l in libri_noleggiati:
            result.append({
                "id": l[0],
                "titolo": l[1],
                "autore": l[2],
                "anno": l[3],
            })
        
        return result
    
    @staticmethod
    def crea_utente(nome, cognome, email):
        
        utenti = DBFunctions.importa_utenti()
        emails = [u[3] for u in utenti]

        if email in emails:
            return None
        
        DBFunctions.inserisci_utente(nome, cognome, email)

        utenti_aggiornati = DBFunctions.importa_utenti()
        utente_creato = next((u for u in utenti_aggiornati if u[3] == email), None)

        if utente_creato:
            return Utente(
                id=utente_creato[0],
                nome=utente_creato[1],
                cognome=utente_creato[2],
                email=utente_creato[3],
                libri=utente_creato[4]
            )
        return None

    @staticmethod
    def noleggia_libro(email_utente, id_libro):

        l = DBFunctions.seleziona_libro(id_libro)
        if l is None:
            raise ValueError("Libro non a catalogo.")
        
        u = DBFunctions.seleziona_utente(email_utente)
        if u is None:
            raise ValueError("Utente non registrato.")
        
        utente = Utente(
            id=u[0],
            nome=u[1],
            cognome=u[2],
            email=u[3],
            libri=u[4])

        libro = Libro(
            id=l[0], 
            titolo=l[1],
            autore=l[2],
            anno=l[3],
            disponibile=l[4]) 
        
        result = DBFunctions.noleggia_libro(id_libro, utente.id, date.today())
        
        if result == "libro_non_disponibile":
            raise ValueError("Libro non disponibile.")
        elif result == "limite_raggiunto":
            raise ValueError("Hai raggiunto il limite massimo di libri.")
        
        return NoleggioResponse(
            utente=utente,
            libro=libro
        )
    
    @staticmethod
    def restituisci_libro(email_utente, id_libro):

        l = DBFunctions.seleziona_libro(id_libro)
        if l is None:
            raise ValueError("Libro non a catalogo.")
        
        u = DBFunctions.seleziona_utente(email_utente)
        if u is None:
            raise ValueError("Utente non registrato.")
        
        utente = Utente(
            id=u[0],
            nome=u[1],
            cognome=u[2],
            email=u[3],
            libri=u[4])

        libro = Libro(
            id=l[0], 
            titolo=l[1],
            autore=l[2],
            anno=l[3],
            disponibile=l[4]) 
        
        p = DBFunctions.restituisci_libro(utente.id, libro.id, date.today())
        if p == "libro_gia_disponibile":
            raise ValueError(f"Libro già disponibile.")
        elif p == "prestito_non_trovato":
            raise ValueError("Prestito non trovato")
        
        return RestituisciResponse(
            status=True
        )

            