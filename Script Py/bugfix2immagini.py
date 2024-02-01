from bs4 import BeautifulSoup
import os

def crea_indice_cartella(directory):
    indice = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            indice.append(file_path)
    return indice

def correggi_url(file_path, indice):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        for img_tag in soup.find_all('img'):
            if 'src' in img_tag.attrs:
                src = img_tag['src']
                print(f"Original src: {src}")

                nome_file = os.path.basename(src)
                file_trovato = next((file for file in indice if nome_file in file), None)

                if file_trovato:
                    # Calcola il percorso relativo tra i file
                    rel_path_parts = os.path.relpath(file_trovato, os.path.dirname(file_path)).split(os.path.sep)
                    rel_path = '/'.join(rel_path_parts)
                    
                    # Aggiorna l'attributo 'src'
                    img_tag['src'] = rel_path
                    print(f"Updated src: {img_tag['src']}")
                else:
                    print(f"File non trovato nel indice: {nome_file}")

            if 'srcset' in img_tag.attrs:
                srcset = img_tag['srcset']
                print(f"Original srcset: {srcset}")

                srcset_elements = srcset.split(',')
                updated_srcset = []

                for element in srcset_elements:
                    element_url = element.strip().split(' ')[0]
                    nome_file = os.path.basename(element_url)

                    file_trovato = next((file for file in indice if nome_file in file), None)

                    if file_trovato:
                        # Calcola il percorso relativo tra i file
                        rel_path_parts = os.path.relpath(file_trovato, os.path.dirname(file_path)).split(os.path.sep)
                        rel_path = '/'.join(rel_path_parts)
                        
                        # Aggiorna l'URL dell'elemento
                        updated_element_url = rel_path
                        updated_srcset.append(updated_element_url)
                    else:
                        print(f"File non trovato nel indice: {nome_file}")

                # Aggiorna l'attributo 'srcset' con gli elementi modificati
                img_tag['srcset'] = ', '.join(updated_srcset)
                print(f"Updated srcset: {img_tag['srcset']}")

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

def elabora_cartella(directory):
    indice = crea_indice_cartella(directory)

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower() == 'index.html':
                file_path = os.path.join(root, filename)
                correggi_url(file_path, indice)

# Esegui l'elaborazione per la tua cartella e tutte le sottocartelle
cartella_principale = r'Percorso directory principale'
elabora_cartella(cartella_principale)
