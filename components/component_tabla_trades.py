import polars as pl
from dash import dcc
import plotly.graph_objects as go
from utils.utils import colores_hex


def returned_tablas_trades(df_summary_winrate: pl.DataFrame) -> dcc.Graph:
    df_summary_winrate = df_summary_winrate.filter(pl.col("Instrumento").is_in(["S&P 500", "EURUSD", "BTCUSD","XAUUSD", "PORTAFOLIO"]))    
    operaciones = df_summary_winrate["Operaciones"].to_list()
    aciertos = df_summary_winrate["Aciertos"].to_list()
    instrumentos = df_summary_winrate["Instrumento"].to_list()

    row_colors = [colores_hex["spx"], colores_hex["eurusd"], colores_hex["btcusd"], colores_hex["xauusd"], colores_hex["portafolio"]]
    
    text_colors = ['black', 'black', 'black', 'black', 'black']

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Instrumentos', 'Trades', 'Wins'],
            fill_color='#374352',
            # fill_color='#34495E', # Lighter/Softer than #212C39
            font=dict(color='white', size=14),
            align='center',
            height=35
        ),
        cells=dict(
            values=[instrumentos, operaciones, aciertos],
            fill_color=[row_colors] * 3, # Same row colors for all 3 columns
            font=dict(color=[text_colors] * 3, size=13, weight='bold'),
            align='center',
            height=30
        )
    )])

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        style={'height': '95%', 'width': '95%'}
    )
