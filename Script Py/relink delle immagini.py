from bs4 import BeautifulSoup
import os

def rimuovi_inizio_url(file_path):
    print(f"Elaborazione del file: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        # Leggi il contenuto del file
        content = file.read()

        # Utilizza BeautifulSoup per analizzare l'HTML
        soup = BeautifulSoup(content, 'html.parser')

        # Trova e aggiorna l'attributo 'src' e 'srcset' per ogni elemento <img>
        for img_tag in soup.find_all('img'):
            # Aggiorna 'src' se presente
            src = img_tag.get('src', '')
            if src.startswith('https://digipass.regione.umbria.it/'):
                new_src = src[len('https://digipass.regione.umbria.it/'):]
                img_tag['src'] = new_src

            # Aggiorna 'srcset' se presente
            srcset = img_tag.get('srcset', '')
            if srcset.startswith('https://digipass.regione.umbria.it/'):
                new_srcset = srcset[len('https://digipass.regione.umbria.it/'):]
                img_tag['srcset'] = new_srcset

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
                rimuovi_inizio_url(file_path)

# Sostituisci 'percorso_della_tua_cartella' con il percorso della cartella che contiene i tuoi file HTML
elabora_cartella('C:\Users\giuli\Desktop\digipass.regione.umbria.it')