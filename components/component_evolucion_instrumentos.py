import polars as pl 
from dash import dcc 
import plotly.graph_objects as go
from datetime import datetime
from functions.backtesting import evolucion
from utils.utils import colores_hex 


def returned_evolucion_instrumentos(df_spx: pl.DataFrame, df_eur: pl.DataFrame, df_btc: pl.DataFrame, df_xau: pl.DataFrame,
                                    fecha_ini: datetime.date, fecha_fin: datetime.date) -> dcc.Graph:
    df = evolucion(df_spx=df_spx, df_eur=df_eur, df_btc=df_btc, df_xau=df_xau)
    df = df.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))
    fig = go.Figure()

    # BTCUSD Trace
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["btc_Monto_ini"],
        mode='lines',
        name='BTCUSD',
        line=dict(color=colores_hex['btcusd'])
    ))

    # EURUSD Trace
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["eur_Monto_ini"],
        mode='lines',
        name='EURUSD',
        line=dict(color=colores_hex['eurusd'])
    ))

    # XAUUSD Trace
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["xau_Monto_ini"],
        mode='lines',
        name='XAUUSD',
        line=dict(color=colores_hex['xauusd'])
    ))

    # SPX Trace
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["spx_Monto_ini"],
        mode='lines',
        name='S&P 500',
        line=dict(color=colores_hex['spx'])
    ))

    fig.update_layout(
        title={
            'text': "Evolución por Instrumentos <br> (2500$ inicial c/instrumento el 01/08/2025)",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=16, 
                color='white'
            )
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            font=dict(color="white"),
            bgcolor='rgba(0,0,0,0)'
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
             tickfont=dict(color='#8F9BA3')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2c3e50',
            gridwidth=1,
            zeroline=False,
             tickfont=dict(color='#8F9BA3')
        ),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        style={'height': '100%', 'width': '100%'}
    )