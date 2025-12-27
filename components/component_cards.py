from dash import html
from datetime import datetime
import polars as pl
from utils.utils import colores_hex
#  ✅   ❌  ▲  ▼


def retorna_card(df: pl.DataFrame, habiles_anio: int) -> html.Div:
    dias_operados = df.shape[0]
    mask = df["date"] == df["date"].min()
    precio_inicial = df.filter(mask)["close"][0]
    monto_inicial = df.filter(mask)["Monto_ini_dia"][0]
    mask = df["date"] == df["date"].max()
    precio_final = df.filter(mask)["close"][0]
    monto_final = df.filter(mask)["Monto_fin_dia"][0]

    var_precio = (precio_final - precio_inicial) / precio_inicial
    var_monto = (monto_final - monto_inicial) / monto_inicial
    var_anual = (var_monto / dias_operados) * habiles_anio

    color = colores_hex["up"] if var_monto > 0 else colores_hex["down"]

    component_card = html.Div(
        [
            html.P(f"Var Instrumento: {var_precio * 100:.2f}%", style={"color": "black"}),
            html.P([
                html.Span("Profit %: ", style={"color": "black"}),
                html.Span(f"{'▲' if var_monto > 0 else '▼'}{var_monto * 100:.2f}%", style={"color": color})
            ]),
            html.P([
                html.Span("Anual %: ", style={"color": "black"}),
                html.Span(f"{'▲' if var_anual > 0 else '▼'}{var_anual * 100:.2f}%", style={"color": color})
            ]),
        ], className="cards"
    )
    return component_card