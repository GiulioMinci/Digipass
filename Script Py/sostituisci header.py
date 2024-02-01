from bs4 import BeautifulSoup
import os

def update_meta_tags_in_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Leggi il contenuto del file HTML
        html_content = file.read()

    # Analizza il contenuto HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Trova tutti i tag 'meta' con l'attributo 'property'
    meta_tags = soup.find_all('meta', property=True)

    # Aggiorna i tag 'meta'
    for tag in meta_tags:
        # Verifica se il tag ha già una barra alla fine e non è vuoto
        if tag.contents and not tag.contents[-1].strip().endswith("/"):
            tag.append("/")

    # Salva le modifiche nel file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))
        print(f"Aggiornato {file_path}")

def update_meta_tags_in_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                update_meta_tags_in_html(file_path)

if __name__ == "__main__":
    # Imposta il percorso della directory principale in modo relativo usando una stringa grezza
    directory_principale = r"C:\Users\giuli\Desktop\digipass.regione.umbria.it\1maggiodigitale-maratona-di-eventi-online-dei-digipass-umbria"

    # Chiama la funzione per aggiornare tutti i file nella directory e sottodirectory
    update_meta_tags_in_directory(directory_principale)
