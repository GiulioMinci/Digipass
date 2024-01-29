from bs4 import BeautifulSoup, Comment
import os

def rimuovi_commenti(file_path):
    print(f"Elaborazione del file: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        # Leggi il contenuto del file
        content = file.read()

        # Utilizza BeautifulSoup per analizzare l'HTML
        soup = BeautifulSoup(content, 'html.parser')

        # Trova e rimuovi i commenti che contengono la parola chiave "HTTrack"
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            if "HTTrack" in comment:
                print("Commento trovato e rimosso:", comment)
                comment.extract()

        # Sovrascrivi il file con il nuovo contenuto
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

    print("Elaborazione completata.")

def elabora_cartella(directory):
    # Percorri tutti i file nella directory e nelle sottocartelle
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.html'):
                file_path = os.path.join(root, filename)
                rimuovi_commenti(file_path)

# Sostituisci 'percorso_della_tua_cartella' con il percorso della cartella che contiene i tuoi file HTML
elabora_cartella ('C:\\Users\\giuli\\Desktop\\digipass.regione.umbria.it')
