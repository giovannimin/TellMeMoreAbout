# -*- coding: utf-8 -*-
"""
Created on 31/07/2023 12:38
@author: GiovanniMINGHELLI
"""
import json
import os
import warnings
from datetime import date

import cairosvg
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from .lib_string import fbref_search_url, PROJECT_NAME
import imageio.v2 as imageio
from io import BytesIO
import matplotlib.pyplot as plt


def get_root(main_project_folder: str = PROJECT_NAME) -> str:
    """
     Retourne le chemin racine du projet principal.

     :param main_project_folder: Nom du dossier principal du projet.
     :return: Le chemin absolu du dossier principal du projet.
     """
    current_directory = os.getcwd()
    while not os.path.exists(os.path.join(current_directory, main_project_folder)):
        current_directory = os.path.dirname(current_directory)
        if current_directory == '/':
            raise FileNotFoundError(f"Repertoire '{main_project_folder}' non-trouve.")
    return os.path.join(current_directory, main_project_folder)


def get_soup(fbref_url=fbref_search_url, name=None):
    """
    :param fbref_url:
    :param name:
    :return:
    """
    if name:
        fbref_url += "=" + name
    response = requests.get(fbref_url)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", response.text), "lxml")

    return soup


def _validate_name(name, url=fbref_search_url):
    """

    :param url:
    :param name:
    :return:
    """
    if not isinstance(name, str):
        raise TypeError("Player name must be a string")
    soup = get_soup(url, name)
    strong_str = [i.next_element for i in soup.findAll("strong")]
    if "0 hits" in strong_str:
        raise ValueError(f"`{name}` not found in FBRef")
    if "Search Results" in strong_str:
        # Grab first search result
        name_soup = soup.find_all("div", class_="search-item-name")
        search_names = [div.find('a').text.strip() for div in name_soup]

        # link_soup = soup.find_all("div", class_="search-item-url")
        # search_url = [div.find('a').text.strip() for div in link_soup]

        msg = f"Exact match for {name} not found.  \n" \
              f"Setting `player_name` to first search result: {search_names[0]}  " \
              f"Maybe `player_name` could be one of them {search_names[1:]}"
        warnings.warn(msg)
        name = search_names[0]

        return _validate_name(name=name, url=url)
    return soup.find("div", id="meta").find('span').text


def get_fbref_url(name):
    """

    :param name:
    :return:
    """
    response = requests.get(fbref_search_url + "=" + name)
    return response.url


def make_scouting_url(player_page_url):
    """

    :param player_page_url:
    :return:
    """
    # Analyser l'URL d'origine
    parsed_url = urlparse(player_page_url)
    # Extraire le chemin de l'URL (partie après le domaine)
    path = parsed_url.path
    # Obtenir la dernière partie du chemin (nom du joueur)
    player_name = path.split('/')[-1]
    # Recuperer la base de l'url
    base_url = '/'.join(parsed_url.path.split('/')[:-1])
    # Construire le nouveau chemin pour le rapport de scouting
    scouting_report_path = f"{base_url}/scout/365_m1/{player_name}-Scouting-Report"
    # Reconstruire l'URL final modifié
    modified_url = parsed_url._replace(path=scouting_report_path)
    return modified_url.geturl()


def calculate_age(birth_date_str):
    birth_date = date.fromisoformat(birth_date_str)
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def get_player_info(url_page: str) -> dict:
    """
    Récupère les informations d'un joueur à partir de l'url_page FBREF spécifiée.
    :param url_page: (str) : L'URL de la page joueur.
    :return: dict: Un dictionnaire contenant les informations du joueur.
              Les clés du dictionnaire sont : 'country', 'position', 'footed', 'weight', 'height', 'img', 'age', 'club'.
              Les informations manquantes auront des valeurs None.
    """
    # Initialiser le dictionnaire pour stocker les informations du joueur
    player_info = {}

    # Utiliser le web scraping pour récupérer les informations disponibles depuis la balise div avec id='info'
    soup = get_soup(url_page)
    player_info['complete_name'] = soup.find("title").next_element.split(" Stats")[0]
    div_tag = soup.find('div', id='info', class_='players')
    if div_tag:
        # Récupérer les tags dispos
        player_info['country'] = div_tag.find('span', class_='f-i').text.strip()
        player_info['country_img'] = re.search(r"url\('(.+?)'\)",
                                               div_tag.find('span', class_='f-i').get('style')).group(1)
        player_info['img'] = div_tag.find("img", class_="").get('src')
        player_info['club'] = div_tag.find('strong', text='Club:').find_next('a').text.strip()
        player_info['age'] = calculate_age(div_tag.find('span', {'id': 'necro-birth'}).get('data-birth'))

        # Parcourir toutes les balises 'p' pour récupérer les informations balisés
        for element in div_tag.find_all('p'):
            text = element.get_text()
            if "Position:" in text:
                # Extraire la position du joueur
                position = text.split("Position:")[-1].strip()
                player_info['position'] = position.split("\xa0▪\xa0")[0].strip()
                footed = position.split("\xa0▪\xa0")[-1].strip()
                if footed.startswith("Footed:"):
                    # Extraire le pied du joueur sans le préfixe 'Footed:'
                    player_info['footed'] = footed[len("Footed: "):].strip()
                else:
                    player_info['footed'] = None
            elif "kg" in text:
                # Extraire le poids du joueur (en kg)
                weight = re.search(r"(\d+)kg", text)
                if weight:
                    player_info['weight'] = weight.group(1)
            elif "cm" in text:
                # Extraire la taille du joueur (en cm)
                height = re.search(r"(\d+)cm", text)
                if height:
                    player_info['height'] = height.group(1)

    try:
        # Utiliser les données JSON pour récupérer les informations les plus fiables et compléter le dictionnaire
        header = soup.find('script', type='application/ld+json')
        if header:
            data = json.loads(header.contents[0])
            player_info.update({'height': data['height']['value'].replace(' cm', ''),
                                'weight': data['weight']['value'].replace(' kg', ''),
                                'age': calculate_age(data['birthDate']),
                                'club': data['memberOf']['name']})
    except (TypeError, KeyError):
        pass

    return player_info


def get_image(img_url: str):
    try:
        response = requests.get(img_url)
        response.raise_for_status()

        if img_url.endswith('.svg'):
            image = cairosvg.svg2png(bytestring=response.content)
            image = imageio.imread(BytesIO(image))
        else:
            image = imageio.imread(BytesIO(response.content))

        return image
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de l'image : {e}")
        return None


def display_img(image: np.ndarray):
    plt.imshow(image)
    plt.axis('off')
    plt.show()


def save_img(image: np.ndarray, output_path: str):
    imageio.imsave(output_path + '.png', image, format='PNG')


def get_slug_id(scouting_url):
    return urlparse(scouting_url).path.split('/')[3]


def get_minutes_played(scouting_url) -> str:
    soup = get_soup(scouting_url)
    if soup.find('div', class_='footer no_hide_long'):
        return soup.find('div', class_='footer no_hide_long').find('strong').text.strip().replace('minutes', '')
    return 'N/A'


def get_available_tables(url, name=None):
    """

    :param url:
    :param name:
    :return:
    """
    soup = get_soup(url, name)
    all_divs = soup.findAll("div", {"class": "table_wrapper"})
    div = tuple([x.find("span")["data-label"] for x in all_divs])
    return div
