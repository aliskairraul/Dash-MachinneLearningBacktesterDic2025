import polars as pl 
from dash import dcc
import plotly.graph_objects as go
from utils.utils import colores_hex
from datetime import datetime

def returned_barras_winrate(df_spx: pl.DataFrame, df_eur: pl.DataFrame, df_btc: pl.DataFrame, df_xau: pl.DataFrame,
                            fecha_ini: datetime.date, fecha_fin: datetime.date) -> dcc.Graph:
    df_spx = df_spx.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))
    df_eur = df_eur.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))
    df_btc = df_btc.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))
    df_xau = df_xau.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))
    rate_spx = round((df_spx["wins_dia"].sum() / df_spx["trades_dia"].sum() * 100), 2) if df_spx["trades_dia"].sum() > 0 else 0
    rate_eur = round((df_eur["wins_dia"].sum() / df_eur["trades_dia"].sum() * 100), 2) if df_eur["trades_dia"].sum() > 0 else 0
    rate_btc = round((df_btc["wins_dia"].sum() / df_btc["trades_dia"].sum() * 100), 2) if df_btc["trades_dia"].sum() > 0 else 0
    rate_xau = round((df_xau["wins_dia"].sum() / df_xau["trades_dia"].sum() * 100), 2) if df_xau["trades_dia"].sum() > 0 else 0
    instrumentos = ["S&P 500", "EURUSD", "BTCUSD","XAUUSD"]
    winrates = [rate_spx, rate_eur, rate_btc, rate_xau]
    min_winrate = min(winrates)
    max_winrate = max(winrates)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=instrumentos,
        y=winrates,
        marker_color=[colores_hex["spx"], colores_hex["eurusd"], colores_hex["btcusd"], colores_hex["xauusd"]],
    ))

    fig.update_layout(
        title={
            'text': "WinRates por Instrumento",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=16,
                color='white'
            )
        },
        yaxis=dict(
            range=[min_winrate * 0.9, max_winrate * 1.1],
            showgrid=True,
            gridcolor='#2c3e50', 
            gridwidth=1,
            zeroline=False,
            visible=True,
            tickfont=dict(color='#8F9BA3')
        ),
         xaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=True,
            tickfont=dict(color='#8F9BA3')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        style={'height': '100%', 'width': '100%'}
    )
