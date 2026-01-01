import polars as pl
from dash import html, dcc
import plotly.graph_objects as go
from datetime import datetime
from functions.backtesting import evolucion


def returned_evolucion_patrimonio(df_spx: pl.DataFrame, df_eur: pl.DataFrame, df_btc: pl.DataFrame,
                                  df_xau: pl.DataFrame, fecha_ini: datetime.date, fecha_fin: datetime.date) -> dcc.Graph:
    df = evolucion(df_spx=df_spx, df_eur=df_eur, df_btc=df_btc, df_xau=df_xau)
    df = df.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))  #
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Monto_ini"],
        fill='tozeroy',
        mode='lines',
        line=dict(color='#79CA7C', width=2),
        fillcolor='rgba(121, 202, 124, 0.1)' 
    ))

    fig.update_layout(
        title={
            'text': "Evolución Patrimonio",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=16,  
                color='white'
            )
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            showgrid=False, 
            zeroline=False,
            visible=True, 
            tickfont=dict(color='#8F9BA3')
        ),
        yaxis=dict(
            showgrid=False, 
            zeroline=False,
            tickfont=dict(color='#8F9BA3')
        )
    )

    component_current_equity = dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        style={'height': '100%', 'width': '100%'},
        id="inner-grafico-portafolio-evolucion"
    )
    
    return component_current_equity
