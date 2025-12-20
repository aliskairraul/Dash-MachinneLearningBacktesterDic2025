import polars as pl 
from dash import dcc
import plotly.graph_objects as go
from utils.utils import colores_hex


def returned_barras_winrate(df_summary_winrate: pl.DataFrame):
    df_summary_winrate = df_summary_winrate.filter(pl.col("Instrumento").is_in(["S&P 500", "EURUSD", "BTCUSD","XAUUSD"]))
    instrumentos = df_summary_winrate["Instrumento"].to_list()
    winrates = df_summary_winrate["Winrate"].to_list()
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
