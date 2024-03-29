# -*- coding: utf-8 -*-
"""
Created on 29/03/2024 12:31
@authors: GiovanniMINGHELLI
"""
from src.player import Player
from src.charts.pizza import Pizza
import argparse


def get_pizza_report(player_name: str):
    player = Player(player_name)
    Pizza(player).plot_pizza_figure(save_fig=True)


def main():
    parser = argparse.ArgumentParser(description="Générer un rapport joueur")
    parser.add_argument("player_name", help="Nom du joueur pour lequel générer le rapport")

    args = parser.parse_args()
    get_pizza_report(args.player_name)


if __name__ == '__main__':
    main()
