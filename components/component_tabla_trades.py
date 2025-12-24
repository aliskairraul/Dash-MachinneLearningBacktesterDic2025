import polars as pl
from dash import dcc
import plotly.graph_objects as go
from utils.utils import colores_hex


def returned_tablas_trades(df_trades: pl.DataFrame, estrategia: str) -> dcc.Graph:
    # df, _ = portafolio_values(df_spx=df_spx, df_eur=df_eur, df_btc=df_btc, df_xau=df_xau)
    # operaciones = [df["spx_trades"].sum(), df["eur_trades"].sum(), df["btc_trades"].sum(), df["xau_trades"].sum(), df["Portafolio Trades"].sum()]
    # aciertos = [df["spx_wins"].sum(), df["eur_wins"].sum(), df["btc_wins"].sum(), df["xau_wins"].sum(), df["Portafolio Wins"].sum()]
    operaciones = []
    aciertos = []
    if estrategia == "Individual":
        operaciones = [df_trades["spx_trades"].sum(), df_trades["eur_trades"].sum(), df_trades["btc_trades"].sum(), df_trades["xau_trades"].sum(), 
                       df_trades["Portafolio Trades"].sum()]
        aciertos = [df_trades["spx_wins"].sum(), df_trades["eur_wins"].sum(), df_trades["btc_wins"].sum(), df_trades["xau_wins"].sum(), 
                    df_trades["Portafolio Wins"].sum()]               
    else:
        operaciones = [df_trades["spx_mayoria_trades"].sum(), df_trades["eur_mayoria_trades"].sum(), df_trades["btc_mayoria_trades"].sum(),
                       df_trades["xau_mayoria_trades"].sum(), df_trades["Portafolio Trades Mayoria"].sum()]
        
        aciertos = [df_trades["spx_mayoria_wins"].sum(), df_trades["eur_mayoria_wins"].sum(), df_trades["btc_mayoria_wins"].sum(),
                    df_trades["xau_mayoria_wins"].sum(), df_trades["Portafolio Wins Mayoria"].sum()]               
    
    instrumentos = ["S&P 500", "EURUSD", "BTCUSD","XAUUSD", "PORTAFOLIO"]

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
