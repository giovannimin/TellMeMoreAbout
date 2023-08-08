# -*- coding: utf-8 -*-
"""
Created on 03/08/2023 19:15
@author: GiovanniMINGHELLI
"""

from src.player import Player
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
from src.lib_string import convert_var_name_to_french
import matplotlib.colors as mcolors
from PIL import Image
import numpy as np



class Pizza:
    def __init__(self, player: Player):
        self.title_size = None
        self.player = player

    def process_data(self):
        data = self.player.get_scouting_report()
        data = data.drop(data[data["statistic"] == ""].index)
        data.set_index("statistic", inplace=True)
        data.rename(index=convert_var_name_to_french, inplace=True)
        return data

    def fit_size(self):
        # caluler les tailles de textes pour automatiser
        self.title_size = 7
        return self.title_size

    @staticmethod
    def _set_color_gradient(values):
        colors = [mcolors.to_hex(mcolors.hsv_to_rgb([(i / 99) * 0.3, 1, 0.85])) for i in range(100)]
        color_mapping = {i: color for i, color in zip(range(101), colors)}
        return [color_mapping[value] for value in values]

    @staticmethod
    def _resize_img(image, desired_width = 100):
        aspect_ratio = image.width / image.height
        desired_height = int(desired_width / aspect_ratio)
        image_np_resized = np.array(image.resize((desired_width, desired_height)))
        return image_np_resized

    def plot_pizza_figure(self):
        data = self.process_data()

        baker = PyPizza(
            params=data.index.to_list(),
            straight_line_color="#000000",
            straight_line_lw=1,
            last_circle_lw=1,
            other_circle_lw=1,
            other_circle_ls="-."
        )
        values = [int(x) for x in data.percentile]
        fig, ax = baker.make_pizza(
            values=values,
            figsize=(8, 8),
            param_location=110,
            slice_colors= self._set_color_gradient(values),
            kwargs_slices=dict( edgecolor="#000000",
                                zorder=2, linewidth=1
                                ),
            kwargs_params=dict(
                color="#000000", fontsize=7,
                va="center", alpha=.9,
            ),
            kwargs_values=dict(
                color="#000000", fontsize=7,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000", facecolor="#F0F0F0",
                    boxstyle="round,pad=0.2", lw=1, alpha=.9,
                )
            )
        )

        fig.text(
            0.515, 0.97, f"{self.player.complete_name} - {self.player.club}", size=18,
            ha="center", color="#000000"
        )

        fig.text(
            0.515, 0.942, f"Per 90 Percentile Rank | 365 last days | {self.player.minutes_played} "
                          f"minutes played", size=15,
            ha="center", color="#000000"
        )

        fig.text(
            0.99, 0.005, f"Players only with more than 15 90s\ndata: Opta from FBref\n"
                         f"Player compared to positional peers in Men's Big 5 Leagues, "
                         f"UCL, UEL over the last 365 days.", size=8,
            color="#000000",
            ha="right"
        )

        fig.figimage(self._resize_img(image=Image.open('player_img.png')), xo=20, yo=20, zorder=-10, alpha=1)
        fig.figimage(self._resize_img(image=Image.open('country_img.png'), desired_width=40), xo=130, yo=20, zorder=-10, alpha=1)

        # plt.savefig(filename, dpi=500, bbox_inches='tight')
        plt.show()
