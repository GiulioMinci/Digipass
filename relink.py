from bs4 import BeautifulSoup
import os
import re

# Variabile globale per contare le rimozioni
rimozioni_totali = 0

def rimuovi_inizio_url(file_path):
    global rimozioni_totali  # Dichiarazione della variabile globale

    print(f"Elaborazione del file: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        # Leggi il contenuto del file
        content = file.read()

        # Utilizza BeautifulSoup per analizzare l'HTML
        soup = BeautifulSoup(content, 'html.parser')

        # Trova e aggiorna l'attributo 'src' e 'srcset' per ogni elemento <img>
        for img_tag in soup.find_all('img'):
            # Verifica la presenza dell'attributo 'src'
            if 'src' in img_tag.attrs:
                # Aggiorna 'src' se presente
                src = img_tag['src']
                print(f"Original src: {src}")

                if src.startswith('https://digipass.regione.umbria.it/wp-content'):
                    new_src = '../wp-content' + src[len('https://digipass.regione.umbria.it/wp-content'):]
                    img_tag['src'] = new_src

                    # Aggiorna il conteggio globale
                    rimozioni_totali += 1

                # Stampa il valore aggiornato
                print(f"Updated src: {img_tag['src']}")

            # Verifica la presenza dell'attributo 'srcset'
            if 'srcset' in img_tag.attrs:
                # Aggiorna 'srcset' se presente
                srcset = img_tag['srcset']
                print(f"Original srcset: {srcset}")

                # Utilizza una regex per trovare e rimuovere l'inizio di ogni origine in 'srcset'
                updated_srcset, num_rimozioni = re.subn(r'https://digipass.regione.umbria.it/wp-content', '../wp-content', srcset, flags=re.IGNORECASE)
                img_tag['srcset'] = updated_srcset

                # Aggiorna il conteggio globale
                rimozioni_totali += num_rimozioni

                # Stampa il valore aggiornato
                print(f"Updated srcset: {img_tag['srcset']}")

        # Sovrascrivi il file con il nuovo contenuto
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

    print("Elaborazione completata.")

def elabora_cartella(directory):
    global rimozioni_totali  # Dichiarazione della variabile globale

    # Percorri tutti i file nella directory e nelle sottocartelle
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.html'):
                file_path = os.path.join(root, filename)
                rimuovi_inizio_url(file_path)

    print(f"Totale rimozioni: {rimozioni_totali}")

# Esegui l'elaborazione per la tua cartella e tutte le sottocartelle
elabora_cartella(r'C:\Users\giuli\Desktop\digipass.regione.umbria.it')
