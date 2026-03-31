import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

class DBFunctions:
    
    #Stringa di connessione
    conn = pyodbc.connect(os.environ["CONN_STR"])

    cursor = conn.cursor()

    @classmethod
    def importa_catalogo(cls):
        cls.cursor.execute("SELECT * FROM Libri;")
        return cls.cursor.fetchall()
    
    @classmethod
    def importa_libri_noleggiati(cls):
        cls.cursor.execute("SELECT id_libro, titolo, autore, anno FROM Libri WHERE disponibile = 0;")
        return cls.cursor.fetchall()
    
    @classmethod
    def importa_utenti(cls):
        cls.cursor.execute("SELECT * FROM Utenti;")
        return cls.cursor.fetchall()
    
    @classmethod
    def inserisci_utente(cls, nome, cognome, email):
        cls.cursor.execute("INSERT INTO Utenti (nome, cognome, email, libri_noleggiati) VALUES (?, ?, ?, ?);", (nome, cognome, email, 0))
        cls.conn.commit()
    
    @classmethod
    def seleziona_libro(cls, id_libro):
        cls.cursor.execute("SELECT * from Libri WHERE id_libro = (?);", id_libro)
        return cls.cursor.fetchone()
    
    @classmethod
    def seleziona_prestito(cls, id_utente):
        cls.cursor.execute("SELECT u.nome, u.cognome, l.id_libro, " 
                        "l.titolo FROM Prestiti p " 
                        "INNER JOIN libri l ON p.id_libro = l.id_libro " 
                        "INNER JOIN utenti u ON p.id_utente = u.id_utente " 
                        "WHERE u.id_utente = (?) AND p.data_restituzione IS NULL;", id_utente)
        return cls.cursor.fetchall()

    @classmethod
    def seleziona_utente(cls, email):
        cls.cursor.execute("SELECT * from Utenti WHERE email = (?);", email)
        return cls.cursor.fetchone()
    
    @classmethod
    def noleggia_libro(cls, id_libro, id_utente, data_p):
        try:
            cls.conn.autocommit = False
            
            rows_libro = cls.cursor.execute("UPDATE Libri " 
                                            "SET disponibile = 0 " 
                                            "WHERE id_libro = (?) AND disponibile = 1;", (id_libro,)).rowcount #BEGIN
            if rows_libro == 0:
                cls.conn.rollback()
                return "libro_non_disponibile"
            row_utente = cls.cursor.execute("UPDATE Utenti " 
                                            "SET libri_noleggiati = libri_noleggiati + 1 " 
                                            "WHERE id_utente = (?) AND libri_noleggiati < 1;", (id_utente,)).rowcount
            if row_utente == 0:
                cls.conn.rollback()
                return "limite_raggiunto" 
            cls.cursor.execute("INSERT INTO Prestiti (id_libro, id_utente, data_prestito) "
                               "VALUES (?, ?, ?);", (id_libro, id_utente, data_p))

            cls.conn.commit() #COMMIT
            return "ok"
        
        except Exception as e:
            cls.conn.rollback() #ROLLBACK
            raise e
        finally:
            cls.conn.autocommit = True
    
    @classmethod
    def restituisci_libro(cls, id_utente, id_libro, data_r):
        try:
            cls.conn.autocommit = False

            rows_libro = cls.cursor.execute("UPDATE Libri " 
                                            "SET disponibile = 1 " 
                                            "WHERE id_libro = (?) AND disponibile = 0;", (id_libro,)).rowcount
            if rows_libro == 0:
                cls.conn.rollback()
                return "libro_gia_disponibile"
        
            rows_prestito = cls.cursor.execute("UPDATE Prestiti "
                            "SET data_restituzione = (?) " 
                            "WHERE id_libro = (?) AND id_utente = (?) AND data_restituzione IS NULL;", (data_r, id_libro, id_utente)).rowcount
            if rows_prestito == 0:
                cls.conn.rollback()
                return "prestito_non_trovato"
            
            cls.cursor.execute("UPDATE Utenti "
                               "SET libri_noleggiati = libri_noleggiati - 1 "
                               "WHERE id_utente = (?) AND libri_noleggiati >= 0;", (id_utente,))
            
            cls.conn.commit()
            return "ok"
        except Exception as e:
            cls.conn.rollback()
            raise e
        finally:
            cls.conn.autocommit = True

    