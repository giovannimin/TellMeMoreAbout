# -*- coding: utf-8 -*-
"""
Created on 31/07/2023 12:38
@author: GiovanniMINGHELLI
"""
import warnings
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from .lib_string import fbref_search_url


def get_soup(fbref_url, name=None):
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
    title = soup.find("title")
    if "0 hits" in strong_str:
        raise ValueError(f"`{name}` not found in FBRef")
    if "Search Results" in title.next_element:
        # Grab first search result
        name_soup = soup.findAll("div", {"class": "search-item-alt-names"})
        search_names = [name_soup[i].contents[0] for i in range(len(name_soup))]
        msg = f"Exact match for {name} not found.  \n" \
              f"Setting `player_name` to first search result: {search_names[0]}  " \
              f"Maybe `player_name` could be one of them {search_names}"
        warnings.warn(msg)
        name = search_names[0]
        return _validate_name(url, name)
    return title.next_element.split(" Stats")[0]


def get_fbref_url(name, url=fbref_search_url):
    """

    :param url: (str): URL de la page de recherche FBREF
    :param name: (str): Nom du joueur
    :return: (str): real fbref url
    """
    # Configation des paramètres de chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigation sur l'URL
    driver.get(url + "=" + name)
    driver.implicitly_wait(2)

    # Récupérer l'URL courante du navigateur une fois que vous êtes sur le site
    current_url = driver.current_url

    # Fermeture de la session
    driver.quit()
    return current_url


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


def get_slug_id(scouting_url):
    return urlparse(scouting_url).path.split('/')[3]


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
