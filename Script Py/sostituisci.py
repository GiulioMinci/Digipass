from bs4 import BeautifulSoup

def replace_id_with_list(html_path, output_path):
    # Carica il contenuto HTML
    with open(html_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # Carica l'output della lista
    with open(output_path, 'r', encoding='utf-8') as output_file:
        list_content = output_file.read()

    # Utilizza BeautifulSoup per analizzare il contenuto HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Sostituisci l'id desiderato con la lista
    content_wrapper = soup.find('div', id='tribe-events-content-wrapper')
    if content_wrapper:
        content_wrapper['id'] = 'new-id'  # Sostituisci con il nuovo id desiderato
        content_wrapper.clear()  # Rimuovi il contenuto attuale del tag
        content_wrapper.append(BeautifulSoup(list_content, 'html.parser'))  # Aggiungi la lista generata

        # Salva il file HTML modificato
        with open('output_modified.html', 'w', encoding='utf-8') as modified_file:
            modified_file.write(str(soup))

if __name__ == "__main__":
    html_path = r'C:\Users\giuli\Desktop\digipass.regione.umbria.it\wordpress-eventi\index.html'
    output_path = 'output.html'  # Assicurati di avere l'output corretto generato in precedenza
    replace_id_with_list(html_path, output_path)
