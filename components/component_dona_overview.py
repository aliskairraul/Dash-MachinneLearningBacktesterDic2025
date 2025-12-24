import polars as pl
from dash import html, dcc
import plotly.graph_objects as go
from utils.utils import colores_hex   # claves del diccionario "eurusd", "btcusd", "xauusd", "spx"


def returned_dona_overview(df_spx: pl.DataFrame, df_eur: pl.DataFrame, df_btc: pl.DataFrame, df_xau: pl.DataFrame) -> dcc.Graph:
    monto_btc = round((df_btc["Monto_fin_dia"][-1]), 2)
    monto_eur = round((df_eur["Monto_fin_dia"][-1]), 2)
    monto_spx = round((df_spx["Monto_fin_dia"][-1]), 2)
    monto_xau = round((df_xau["Monto_fin_dia"][-1]), 2)
    monto_portafolio = int(monto_btc + monto_eur + monto_spx + monto_xau)
    monto_inicial = int(df_btc["Monto_ini_dia"][0] + df_eur["Monto_ini_dia"][0] + df_spx["Monto_ini_dia"][0] + df_xau["Monto_ini_dia"][0])

    # Determinar color del monto portafolio
    color_portafolio = colores_hex["up"] if monto_portafolio > monto_inicial else colores_hex["down"]

    # Datos para el gráfico
    labels = ["BTCUSD", "EURUSD", "S&P 500", "XAUUSD"]
    values = [monto_btc, monto_eur, monto_spx, monto_xau]
    colors = [colores_hex["btcusd"], colores_hex["eurusd"], colores_hex["spx"], colores_hex["xauusd"]]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.8,
        marker=dict(colors=colors, line=dict(color='#000000', width=0)),
        sort=False,
        textinfo='none',
        hovertemplate='<b>%{label}</b><br>Monto: $%{value:,.2f}<br>Participación Relativa: %{percent}<extra></extra>'
    )])

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10, b=10, l=10, r=10),
        annotations=[
            dict(
                text=f"${monto_portafolio:,}",
                x=0.5, y=0.55,
                font=dict(size=24, color=color_portafolio, weight="bold"),
                showarrow=False
            ),
            dict(
                text=f"Ini: ${monto_inicial:,}",
                x=0.5, y=0.40,
                font=dict(size=14, color="rgb(143, 155, 163)"),
                showarrow=False
            )
        ]
    )

    component_dona_overview = dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        style={'height': '100%', 'width': '100%'},
        id="dona-overview"
    )
    
    return component_dona_overview


