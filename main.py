from DBfunctions import *
from fastapi import FastAPI, Depends, HTTPException
from oggetti import NoleggioRequest, UtenteCreate, RestituisciRequest
from BibliotecaService import BibliotecaService

app = FastAPI()

def get_service():
    return BibliotecaService()

@app.get("/libri")
def get_libri(service: BibliotecaService = Depends(get_service)):
    return service.get_libri()

@app.get("/libri-noleggiati")
def get_libri_noleggiati(service: BibliotecaService = Depends(get_service)):
    return service.get_libri_noleggiati()

@app.post("/utenti")
def crea_utente(u: UtenteCreate, service: BibliotecaService = Depends(get_service)):
    utente = service.crea_utente(u.nome, u.cognome, u.email)

    if utente is None:
        raise HTTPException(status_code=400, detail="Utente già registrato")
    
    return utente

@app.post("/noleggia-libro")
def noleggia_libro(req: NoleggioRequest, service: BibliotecaService = Depends(get_service)):
    try:
        noleggio = service.noleggia_libro(req.email, req.libro_id)
        return noleggio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/restituisci-libro")    
def restituisci_libro(req: RestituisciRequest, service: BibliotecaService = Depends(get_service)):
    try:
        return service.restituisci_libro(req.email, req.libro_id)     
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

