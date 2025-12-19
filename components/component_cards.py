from dash import html
from datetime import datetime
import polars as pl
from utils.utils import colores_hex
#  ✅   ❌  ▲  ▼


def retorna_card(df: pl.DataFrame) -> html.Div:
    mask = df["date"] == df["date"].min()
    precio_inicial = df.filter(mask)["close"][0]
    monto_inicial = df.filter(mask)["Monto_ini_dia"][0]
    mask = df["date"] == df["date"].max()
    precio_final = df.filter(mask)["close"][0]
    monto_final = df.filter(mask)["Monto_fin_dia"][0]

    var_precio = (precio_final - precio_inicial) / precio_inicial
    var_monto = (monto_final - monto_inicial) / monto_inicial

    color = colores_hex["up"] if var_monto > 0 else colores_hex["down"]

    component_card = html.Div(
        [
            html.P(f"Price Variation: {var_precio * 100:.2f}%", style={"color": "black"}),
            html.P(f"Strategy Return: {'▲' if var_monto > 0 else '▼'}{var_monto * 100:.2f}%", style={"color": color}),
        ], className="cards"
    )
    return component_card