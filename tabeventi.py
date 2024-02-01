import os
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser

def extract_data(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    date_element = soup.find('span', class_='tribe-event-date-start')
    if date_element:
        date_str = date_element.get_text(strip=True)
        date_str = date_str.split(" orario ")[0]

        formatted_date_str = date_str.replace("Gennaio", "January").replace("Febbraio", "February").replace("Marzo", "March").replace("Aprile", "April").replace("Maggio", "May").replace("Giugno", "June").replace("Luglio", "July").replace("Agosto", "August").replace("Settembre", "September").replace("Ottobre", "October").replace("Novembre", "November").replace("Dicembre", "December")

        try:
            date_obj = parser.parse(formatted_date_str, dayfirst=True, fuzzy=True)
        except ValueError as e:
            print(f"Errore nella data per il file: {file_path}")
            date_obj = None
    else:
        date_obj = None

    title_element = soup.find('h1', class_='tribe-events-single-event-title')
    title = title_element.get_text(strip=True) if title_element else None

    categories_elements = soup.find_all('dd', class_='tribe-events-event-categories')
    categories = ', '.join(category.get_text(strip=True) for category in categories_elements) if categories_elements else None

    return title, date_obj, categories

def generate_html_output(file_list):
    html_content = """
<html>
<head>
    <title>File Date Extraction</title>
</head>
<body>
    <div id="outputContainer">
        <table id="ricercaevento" class="display">
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Organizzatore</th>
                </tr>
            </thead>
            <tbody>
"""

    for title, _, _, categories, clickable_path in file_list:
        html_content += f"<tr data-organizzatore='{categories}'><td><a href='{clickable_path}'>{title}</a></td><td>{categories}</td></tr>"

    html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""

    try:
        with open('output.html', 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
    except Exception as e:
        print(f"Errore durante la scrittura del file HTML: {e}")

def main():
    root_folder = r'C:\\Users\\giuli\\Desktop\\digipass.regione.umbria.it\\wordpress-eventi'
    file_list = []

    for root, dirs, files in os.walk(root_folder):
        for file_name in files:
            if file_name.endswith('.html'):
                file_path = os.path.join(root, file_name)
                title, date, categories = extract_data(file_path)
                if title and date:
                    print(f"Processing file: {file_path}")
                    file_list.append((title, date, categories, file_path))

    sorted_files = sorted(file_list, key=lambda x: x[1], reverse=True)
    generate_html_output(sorted_files)

if __name__ == "__main__":
    main()
