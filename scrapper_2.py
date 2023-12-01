from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random  # Importer la bibliothèque random

def scrape_titles_all_pages(base_url, max_pages=None):
    # Configurer les options du navigateur
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter le navigateur en mode sans tête (headless)

    # Initialiser le navigateur
    driver = webdriver.Chrome(options=chrome_options)

    # Liste pour stocker les données de toutes les pages
    all_data = []

    # Boucle pour parcourir les pages
    current_page = 1
    while True:
        # Construire l'URL de la page actuelle
        url = f"{base_url}&page={current_page}"

        # Charger la page web
        driver.get(url)

        # Attendre que les blocs spécifiques soient présents dans le DOM
        wait = WebDriverWait(driver, 10)
        target_blocks = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.sc-bXCLTC.kkKAOM.ais-Hits-list-item')))

        # Obtenir le contenu HTML après que la page a été rendue
        html_content = driver.page_source

        # Utiliser BeautifulSoup pour analyser le HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Créer une liste de dictionnaires avec les données
        data = []
        for block in soup.find_all('li', class_='sc-bXCLTC kkKAOM ais-Hits-list-item'):
            title_div = block.find('div', {'role': 'mark', 'class': 'sc-bXCLTC hlqow9-0 helNZg'})
            company_div = block.find('span', class_='sc-ERObt gTCEVh sc-6i2fyx-3 eijbZE wui-text')
            city_span = block.find('span', class_='sc-68sumg-0 gvkFZv')

            if title_div and company_div and city_span:
                title = title_div.text.strip()
                company = company_div.text.strip()
                city = city_span.text.strip()
                data.append({'Poste': title, 'Entreprise': company, 'Ville': city})

                # Ajouter une pause aléatoire entre 1 et 3 secondes entre chaque collecte
                time.sleep(random.uniform(1, 3))

        # Ajouter les données de la page actuelle à la liste générale
        all_data.extend(data)

        # Si la limite maximale de pages est atteinte, arrêter la boucle
        if max_pages and current_page >= max_pages:
            break

        # Passer à la page suivante
        current_page += 1

    # Fermer le navigateur
    driver.quit()

    # Créer un DataFrame à partir de la liste de dictionnaires
    df = pd.DataFrame(all_data)

    # Imprimer le DataFrame
    print(df)

# URL de la page à scraper
base_url = "https://www.welcometothejungle.com/fr/jobs?refinementList%5Boffices.country_code%5D%5B%5D=FR&query=data"
# Appeler la fonction avec l'URL de base et le nombre maximum de pages (facultatif)
scrape_titles_all_pages(base_url, max_pages=1)
