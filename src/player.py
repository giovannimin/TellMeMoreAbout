# -*- coding: utf-8 -*-
"""
Created on 31/07/2023 12:38
@author: GiovanniMINGHELLI
"""

import pandas as pd
import os
from .utils import get_soup, _validate_name, get_fbref_url, make_scouting_url, get_slug_id, get_player_info, \
    get_minutes_played, get_image, save_img, get_root

root = get_root()


def cache_stats(url, _attr_name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            data = getattr(self, _attr_name)
            if data is None:
                data = self.get_tables(url=getattr(self, url))
                setattr(self, _attr_name, data)
                return func(self, *args, **kwargs)
            else:
                return func(self, *args, **kwargs)

        return wrapper

    return decorator


class Player:
    def __init__(self, player_name):
        self.name = _validate_name(name=player_name)
        self._url_page = get_fbref_url(name=self.name)
        self._standard_tables = None
        self._scouting_url = make_scouting_url(player_page_url=self._url_page)
        self._scouting_tables = None
        self.slug_id = get_slug_id(scouting_url=self._scouting_url)
        self.infos = get_player_info(url_page=self._url_page)
        self.img = self.infos['img']
        self.country_img = self.infos['country_img']
        self.club_img = self.infos['club_img']
        self.position = self.infos['position']
        self.height = self.infos['height']
        self.weight = self.infos['weight']
        self.age = self.infos['age']
        self.club = self.infos['club']
        self.country = self.infos['country']
        self.footed = self.infos['footed']
        self.complete_name = self.infos['complete_name']
        minutes_played_value = get_minutes_played(scouting_url=self._scouting_url)
        self.minutes_played = minutes_played_value if minutes_played_value is not None else None

        save_img(get_image(img_url=self.img), output_path=os.path.join(root, 'assets', 'player_attr',  'player_img'))
        save_img(get_image(img_url=self.country_img), output_path=os.path.join(root, 'assets', 'player_attr', 'country_img'))
        if self.club_img:
            save_img(get_image(img_url=self.club_img), output_path=os.path.join(root, 'assets', 'player_attr', 'club_img'))

    def __repr__(self):
        return "<player: {}, slug_id: {}, id: {}>".format(self.name, self.slug_id, id(self))

    @staticmethod
    def get_tables(url):
        soup = get_soup(url)
        all_tables = soup.findAll("tbody")
        all_headers = soup.findAll("div", {"class": "section_heading"})
        head_labels = [i.span["data-label"] for i in all_headers]

        df_dict = dict()
        for table, label in zip(all_tables, head_labels):
            pre_df_dict = dict()
            rows = table.find_all("tr")
            for row in rows:
                if row.find("th", {"scope": "row"}) is not None:

                    var_name = row.find("th", {"scope": "row"})["data-stat"]
                    var_value = row.find("th", {"scope": "row"}).text.strip()

                    if var_name not in pre_df_dict:
                        pre_df_dict[var_name] = [var_value]
                    else:
                        pre_df_dict[var_name].append(var_value)

                    cells = row.find_all("td")
                    for cell in cells:
                        cell_text = cell.text.encode()
                        text = cell_text.decode("utf-8")
                        try:
                            text = float(text)
                        except ValueError:
                            pass
                        if cell["data-stat"] in pre_df_dict:
                            pre_df_dict[cell["data-stat"]].append(text)
                        else:
                            pre_df_dict[cell["data-stat"]] = [text]

            df = pd.DataFrame.from_dict(pre_df_dict)
            df_dict[f"{label}"] = df
        return df_dict

    @cache_stats(url='_scouting_url', _attr_name='_scouting_tables')
    def get_scouting_report(self):
        return self._scouting_tables['Scouting Report']

    @cache_stats(url='_scouting_url', _attr_name='_scouting_tables')
    def get_complete_scouting_report(self):
        return self._scouting_tables['Complete Scouting Report']

    @cache_stats(url='_scouting_url', _attr_name='_scouting_tables')
    def get_similar_players(self):
        return self._scouting_tables['Similar Players']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_standard_stats(self):
        return self._standard_tables['Standard Stats']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_player_news(self):
        return self._standard_tables['Player News']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_shooting_stats(self):
        return self._standard_tables['Shooting']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_passing_stats(self):
        return self._standard_tables['Passing']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_pass_type_stats(self):
        return self._standard_tables['Pass Types']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_goals_and_shots_stats(self):
        return self._standard_tables['Goal and Shot Creation']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_defensive_stats(self):
        return self._standard_tables['Defensive Actions']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_possession_stats(self):
        return self._standard_tables['Possession']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_playing_time(self):
        return self._standard_tables['Playing Time']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_miscellaneaous_stats(self):
        return self._standard_tables['Miscellaneous Stats']

    @cache_stats(url='_url_page', _attr_name='_standard_tables')
    def get_player_club_summary(self):
        return self._standard_tables['Player Club Summary']
