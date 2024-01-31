from bs4 import BeautifulSoup
import os

def update_link_in_html(file_path, new_url):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Leggi il contenuto del file HTML
        html_content = file.read()

    # Analizza il contenuto HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Trova il tag 'a' con l'attributo 'href' desiderato
    link_tag = soup.find('a', href="https://www.digipass.regione.umbria.it")

    # Se il tag è trovato, sostituisci l'URL
    if link_tag:
        link_tag['href'] = new_url

        # Salva le modifiche nel file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
            print(f"Aggiornato {file_path}")

def update_links_in_directory(directory_path, new_url):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                update_link_in_html(file_path, new_url)

if __name__ == "__main__":
    # Imposta la nuova URL desiderata
    nuova_url = "https://digipass.regione.umbria.it/"

    # Imposta il percorso della directory principale in modo relativo
    directory_principale = "C:/Users/giuli/Desktop/digipass.regione.umbria.it"

    # Chiama la funzione per aggiornare tutti i file nella directory e sottodirectory
    update_links_in_directory(directory_principale, nuova_url)
