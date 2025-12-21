import polars as pl
from dash import html, dcc
import plotly.graph_objects as go


def returned_current_equity(df_evolution_capital: pl.DataFrame) -> dcc.Graph:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_evolution_capital["date"],
        y=df_evolution_capital["Portafolio"],
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
