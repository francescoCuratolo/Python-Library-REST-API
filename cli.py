from utilities import *
import client as c
from tabulate import tabulate

class Menu:
    def __init__(self):
        self.on = True
    
    def run(self):
        self.pagina_iniziale()

    def pagina_iniziale(self):
        while self.on:
            print("\nWelcome to Python Library!\n")

            scelta = Utilities.safe_int(input(
                "1) Mostra catalogo\n" 
                "2) Mostra libri noleggiati\n" 
                "3) Registra utente\n" 
                "4) Noleggia un libro\n" 
                "5) Restituici un libro\n\n" 
                "Premere 0 per uscire.\n").strip())
            
            while scelta < 0 or scelta > 5:
                scelta = Utilities.safe_int(input("\nInserisci un opzione valida.\n").strip())

            if scelta == 0:
                self.on = False
                return
            else:
                match scelta:
                    case 1:
                        self.mostra_catalogo()
                    case 2:
                        self.mostra_libri_noleggiati()
                    case 3:
                        self.registra_utente()
                    case 4:
                        self.noleggia_libro()
                    case 5:
                        self.restituisci_libro()


    def mostra_catalogo(self):
        catalogo = c.mostra_catalogo()
        print(tabulate(
            [[l["id"], l["titolo"], l["autore"], l["anno"], "Si" if l["disponibile"] else "No"] for l in catalogo], 
            headers=["ID", "Titolo", "Autore", "Anno", "Disponibilità"], 
            tablefmt="plain"))
        input("\nPremi invio per continuare...")
              
    def mostra_libri_noleggiati(self):
        libri_noleggiati = c.mostra_libri_noleggiati()
        print(tabulate(
            [[l["id"], l["titolo"], l["autore"], l["anno"]] for l in libri_noleggiati],
            headers=["ID", "Titolo", "Autore", "Anno"]
        ))
        input("\nPremi invio per continuare...")
                
    def registra_utente(self):
        print("\nRegistrazione Utente:\n" 
        "Premere 0 per uscire dalla registrazione.\n")
        
        nome = input("Nome: ").strip()
        if nome == "0":
            return
        cognome = input("Cognome: ").strip()
        if cognome == "0":
            return
        email = input("Email: ").strip()
        if email == "0":
            return

        utente = c.registra_utente(nome, cognome, email)
        if utente:
            print(f"Utente creato: {utente['nome']} {utente['cognome']} ({utente['email']})")
        input("\nPremi invio per continuare...")
    
    def noleggia_libro(self):
        print("\nNoleggia un libro.\n")
        
        id_libro = Utilities.safe_int(input("Inserisci il codice (Id) del libro che vuoi noleggiare (0 per uscire): ").strip())
        if id_libro == 0:
            return
        email = input("Inserisci l'indirizzo email di chi vuole noleggiare il libro (0 per uscire): ").strip()
        if email == "0":
            return

        noleggio = c.noleggia_libro(email, id_libro)
        if noleggio:
            print("Libro noleggiato con successo!")
            print(f"{noleggio["utente"]["nome"]} {noleggio["utente"]["cognome"]} ha noleggiato {noleggio["libro"]["titolo"]}")
        input("\nPremi invio per continuare...")

    def restituisci_libro(self):
        print("\nRestituisci un libro.\n")

        id_libro = Utilities.safe_int(input("Inserisci il codice (Id) del libro che vuoi restituire (0 per uscire): ").strip())
        if id_libro == 0:
            return
        email = input("Inserisci l'indirizzo email di chi vuole restituire il libro: ").strip()
        if email == "0":
            return
        
        restituzione = c.restituisci_libro(email, id_libro)
        if restituzione and restituzione.get("status"):
            print("Libro restituito con successo!")
        input("\nPremi invio per continuare...")
        
def main():
    menu = Menu()
    menu.run()

if __name__ == "__main__":
    main()