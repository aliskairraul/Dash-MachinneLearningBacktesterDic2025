import polars as pl 
from dash import dcc 
import plotly.graph_objects as go 
from utils.utils import colores_hex 

# def returned_evolucion_instrumentos(df_back_spx: pl.DataFrame, df_back_eur: pl.DataFrame, df_back_btc: pl.DataFrame, df_back_xau: pl.DataFrame):
def returned_evolucion_instrumentos(df_evolution_capital: pl.DataFrame):
    fig = go.Figure()

    # BTCUSD Trace
    fig.add_trace(go.Scatter(
        x=df_evolution_capital["date"],
        y=df_evolution_capital["BTCUSD"],
        mode='lines',
        name='BTCUSD',
        line=dict(color=colores_hex['btcusd'])
    ))

    # EURUSD Trace
    fig.add_trace(go.Scatter(
        x=df_evolution_capital["date"],
        y=df_evolution_capital["EURUSD"],
        mode='lines',
        name='EURUSD',
        line=dict(color=colores_hex['eurusd'])
    ))

    # XAUUSD Trace
    fig.add_trace(go.Scatter(
        x=df_evolution_capital["date"],
        y=df_evolution_capital["XAUUSD"],
        mode='lines',
        name='XAUUSD',
        line=dict(color=colores_hex['xauusd'])
    ))

    # SPX Trace
    fig.add_trace(go.Scatter(
        x=df_evolution_capital["date"],
        y=df_evolution_capital["SPX"],
        mode='lines',
        name='S&P 500',
        line=dict(color=colores_hex['spx'])
    ))

    fig.update_layout(
        title={
            'text': "Evolutions per Instruments",
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