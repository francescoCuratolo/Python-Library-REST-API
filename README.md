# Python-Library-REST-API
Python Library REST API è un’applicazione REST API in Python per gestire una piccola biblioteca: permette di visualizzare il catalogo, registrare utenti, noleggiare e restituire libri. Include anche un’interfaccia a riga di comando (CLI) per interagire con l’API.

## Caratteristiche
-	Visualizzazione del catalogo libri e dei libri attualmente noleggiati.
-	Registrazione di nuovi utenti.
-	Noleggio e restituzione libri.
-	Interfaccia REST API tramite FastAPI.
-	Client CLI interattivo per semplificare le operazioni.
-	Persistenza dei dati tramite database SQL gestito con pyodbc.

## Struttura del progetto

├── main.py                -> Entry point API FastAPI

├── client.py              -> Client Python per interagire con l'API

├── cli.py                 -> Interfaccia a riga di comando

├── oggetti.py             -> Modelli Pydantic per richieste e risposte

├── BibliotecaService.py   -> Logica di business della biblioteca

├── DBFunctions.py         -> Funzioni di accesso al database

├── utilities.py           -> Funzioni di utilità (es. validazione input)

├── .env                   -> Variabili d'ambiente (stringa di connessione DB)

└── README.md              # Documentazione progetto

## Requisiti

-	Python 3.10+
-	FastAPI
-	Uvicorn
-	requests
-	pyodbc
-	python-dotenv
-	tabulate

Installazione tramite pip:
~~~
pip install fastapi uvicorn requests pyodbc python-dotenv tabulate
~~~

## Configurazione del Database
Il progetto utilizza pyodbc per connettersi a un database SQL.
Creare un file .env nella root del progetto con la stringa di connessione:
~~~
CONN_STR=Driver={SQL Server Native Client 11.0};Server=TUO_SERVER;Database=Biblioteca;UID=USERNAME;PWD=PASSWORD;
~~~

## Schema del Database
Il database Biblioteca contiene tre tabelle principali: Utenti, Libri e Prestiti.
### Utenti

| Colonna	| Tipo | Vincoli |
| ------- | ----- | ------ |
| id_utente	| INT	| PK, autoincrement, NOT NULL |
| nome |	VARCHAR(100) |	NOT NULL |
| cognome	| VARCHAR(100) |	NOT NULL |
|email	| VARCHAR(100) |	NOT NULL |
| libri_noleggiati	| INT	| CHECK (libri_noleggiati IN (0,1,2)) |

### Libri

| Colonna |	Tipo	| Vincoli |
| ------- | ----- | ------- |
| id_libro |	INT	| PK, autoincrement, NOT NULL |
| titolo	| VARCHAR(100)	| NOT NULL |
| autore |	VARCHAR(100) |	NOT NULL |
| anno |	INT	| NOT NULL |
| disponibile |	BIT/BOOL |	NOT NULL |

### Prestiti

| Colonna |	Tipo	| Vincoli |
| ------- | ---- | -------- |
| id_prestito |	INT |	PK, autoincrement, NOT NULL |
| id_libro |	INT |	FK → Libri.id_libro, NOT NULL |
| id_utente |	INT |	FK → Utenti.id_utente, NOT NULL |
| data_prestito |	DATE |	NOT NULL |
| data_restituzione |	DATE |	NULLABLE |

Relazioni principali:
-	Un utente può avere 0–2 libri noleggiati (Utenti.libri_noleggiati controlla questo limite).
-	Un libro può essere noleggiato da 0 o 1 utente alla volta (Libri.disponibile indica se è disponibile).
-	La tabella Prestiti collega libri e utenti tramite chiavi esterne (id_libro e id_utente) e registra le date di prestito e restituzione.

## Avvio dell’API
Eseguire il server FastAPI:
~~~
uvicorn main:app --reload
~~~
L’API sarà disponibile su http://127.0.0.1:8000.

## Endpoint principali

| Metodo	| Endpoint	| Descrizione |
| ------ | ---------- | ----------- |
| GET |	/libri	| Restituisce il catalogo dei libri |
| GET	| /libri-noleggiati |	Restituisce i libri attualmente noleggiati |
| POST |	/utenti	| Crea un nuovo utente |
| POST |	/noleggia-libro |	Noleggia un libro |
| POST |	/restituisci-libro |	Restituisce un libro |

## CLI Interattiva
Il progetto include un’interfaccia a riga di comando (cli.py) per interagire con l’API:
~~~
python cli.py
~~~
### Funzionalità:
- Mostra catalogo libri
- Mostra libri noleggiati
-	Registra nuovo utente
-	Noleggia un libro
-	Restituisci un libro
-	Esci

## Esempio di utilizzo del client Python
~~~
import client as c

# Mostra catalogo
catalogo = c.mostra_catalogo()
print(catalogo)

# Registra un nuovo utente
utente = c.registra_utente("Mario", "Rossi", "mario.rossi@example.com")
print(utente)

# Noleggia un libro
noleggio = c.noleggia_libro("mario.rossi@example.com", 1)
print(noleggio)

# Restituisci un libro
restituzione = c.restituisci_libro("mario.rossi@example.com", 1)
print(restituzione)
~~~

## Note
-	La logica principale della biblioteca è implementata in BibliotecaService.py.
-	L’accesso al database è gestito in DBFunctions.py.
-	I modelli di dati e le richieste/risposte sono definiti in oggetti.py.
-	La CLI usa tabulate per formattare le tabelle in console.

## Licenza
Distribuito sotto licenza MIT.


