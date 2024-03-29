# -*- coding: utf-8 -*-
"""
Created on 29/03/2024 12:31
@authors: GiovanniMINGHELLI
"""
from src.player import Player
from src.charts.pizza import Pizza


def get_pizza_report(player_name: str):
    player = Player(player_name)
    Pizza(player).plot_pizza_figure(save_fig=True)


if __name__ == '__main__':
    requested = input("> player_name :")
    get_pizza_report(player_name=requested)
