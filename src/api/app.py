# -*- coding: utf-8 -*-
"""
Created on 29/03/2024 14:46
@authors: GiovanniMINGHELLI
"""
import io
import warnings

from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from matplotlib import pyplot as plt

from src.player import Player
from src.charts.pizza import Pizza

warnings.filterwarnings("ignore")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/status")
def get_api_health():
    return {"status": 1}


@app.get("/status/{player_name}")
def get_report(player_name: str, response: Response):
    """

    :param player_name:
    :param response:
    :return:
    """
    player = Player(player_name)
    report = Pizza(player).plot_pizza_figure(save_fig=True)

    if not report:
        raise HTTPException(status_code=404, detail=f"Aucun rapport disponible pour {player_name}")

    # Convertir la figure en format PNG
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    response.headers["Content-Disposition"] = f"attachment; filename={player_name}_report.png"
    response.headers["Content-Type"] = "image/png"

    return Response(content=img_bytes.getvalue(), media_type="image/png")
