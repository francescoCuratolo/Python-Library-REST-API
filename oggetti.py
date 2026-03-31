from pydantic import BaseModel

class Utente(BaseModel):
    id: int
    nome: str
    cognome: str
    email: str
    libri: int

class UtenteCreate(BaseModel):
    nome: str
    cognome: str
    email: str

class Libro(BaseModel):
    id: int
    titolo: str
    autore: str
    anno: int
    disponibile: bool

class NoleggioRequest(BaseModel):
    email: str
    libro_id: int

class NoleggioResponse(BaseModel):
    utente: Utente
    libro: Libro

class RestituisciRequest(BaseModel):
    email: str
    libro_id: int

class RestituisciResponse(BaseModel):
    status: bool