import os
from bs4 import BeautifulSoup
from datetime import datetime
import locale
from dateutil import parser
import gzip

locale.setlocale(locale.LC_TIME, 'it_IT.utf8')

def extract_data(file_path):
    try:
        with gzip.open(file_path, 'rt', encoding='utf-8-sig') as file:
            content = file.read()
    except gzip.BadGzipFile:
        # Se la decompressione fallisce, leggi il file come testo senza decompressione
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Estrai la data
    date_element = soup.find('span', class_='tribe-event-date-start')
    if date_element:
        date_str = date_element.get_text(strip=True)
        date_str = date_str.split(" orario ")[0]

        # Adatta il formato della stringa della data
        formatted_date_str = date_str.replace("Gennaio", "January").replace("Febbraio", "February").replace("Marzo", "March").replace("Aprile", "April").replace("Maggio", "May").replace("Giugno", "June").replace("Luglio", "July").replace("Agosto", "August").replace("Settembre", "September").replace("Ottobre", "October").replace("Novembre", "November").replace("Dicembre", "December")

        try:
            date_obj = parser.parse(formatted_date_str, dayfirst=True, fuzzy=True)
        except ValueError as e:
            print(f"Errore nella data per il file: {file_path}")
            print(f"Dettagli dell'errore: {e}")
            date_obj = None
    else:
        date_obj = None

    # Estrai il titolo
    title_element = soup.find('h1', class_='tribe-events-single-event-title')
    title = title_element.get_text(strip=True) if title_element else None

    return title, date_obj

from itertools import groupby
from operator import itemgetter

def generate_html_output(file_list):
    html_content = '<html><head><title>File Date Extraction</title></head><body>'

    # Ordina la lista in base alla data
    sorted_files = sorted(file_list, key=lambda x: x[1][1])

    html_content += '<div style="list-style-type:none; padding:0; margin:0;">'  # Stile per la lista compatta

    for file_path, (title, date) in sorted_files:
        try:
            if title and date:
                clickable_path = file_path.replace(r'C:\\Users\\giuli\\Desktop\\digipass.regione.umbria.it\\evento', '').replace('\\', '/')
                clickable_path = clickable_path.replace('://', '').replace('../..//', '').lstrip('/')
                
                html_content += f"<h4><a href=\"{clickable_path}\">{title} {date.strftime('%B %Y')}</a></h4>"
        except Exception as ex:
            print(f"Errore durante la generazione dell'output per il file: {file_path}")
            print(f"Dettagli dell'errore: {ex}")

    html_content += '</div>'
    html_content += '</body></html>'

    with open('output.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)


def main():
    root_folder = r'C:\\Users\\giuli\\Desktop\\digipass.regione.umbria.it\\evento'
    file_list = []

    for root, dirs, files in os.walk(root_folder):
        for file_name in files:
            if file_name.endswith('.html'):
                file_path = os.path.join(root, file_name)
                title, date = extract_data(file_path)
                if title or date:
                    file_list.append((file_path, (title, date)))

    sorted_files = sorted(file_list, key=lambda x: x[1][1], reverse=True)

    generate_html_output(sorted_files)

if __name__ == "__main__":
    main()
