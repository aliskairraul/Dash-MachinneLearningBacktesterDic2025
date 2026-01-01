import polars as pl 
from dash import dcc 
import plotly.graph_objects as go 
from functions.backtesting import evolucion
from utils.utils import colores_hex
from datetime import datetime

fecha_inicio = datetime(2025, 8, 1).date()


def returned_evolucion_elegido(df_spx: pl.DataFrame,
                               df_eur: pl.DataFrame,
                               df_btc: pl.DataFrame,
                               df_xau: pl.DataFrame,
                               df_elegido: pl.DataFrame,
                               drop_value: str,
                               fecha_ini: datetime.date,
                               fecha_fin: datetime.date) -> dcc.Graph:
    df = evolucion(df_spx=df_spx, df_eur=df_eur, df_btc=df_btc, df_xau=df_xau)
    df = df.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))
    df_elegido = df_elegido.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))

    # Datos para el tooltip
    dias = df.shape[0]
    trades_tooltip = df_elegido["trades_dia"].sum()
    aciertos_tooltip = df_elegido["wins_dia"].sum()
    winrate_tooltip = round((aciertos_tooltip / trades_tooltip * 100),2)  if trades_tooltip > 0 else 0    
    ganancia_tooltip = df_elegido["Monto_fin_dia"][-1] - df_elegido["Monto_ini_dia"][0]
    profit_tooltip = round(((ganancia_tooltip / df_elegido["Monto_ini_dia"][0]) * 100),2)
    proyeccion_anual_tooltip = round(((profit_tooltip / dias) * 365),2)

    # Data para la grafica
    # titulo_grafica = f"Evolución de {drop_value} Vs Portafolio"
    if df_elegido["date"][0] != fecha_inicio:
        titulo_grafica = f"Modelo: {drop_value}    Vs   Portafolio <br> Ambos comenzaron con 10000$ el 01/08/2025"
    else:
        titulo_grafica = f"Modelo: {drop_value}    Vs   Portafolio"    
    df_elegido = df_elegido.select(["date", "Monto_ini_dia"])
    df_elegido.columns = ["date", drop_value]

    df_evolution_capital = df.select(["date", "Monto_ini"])
    df_evolution_capital = df_evolution_capital.join(df_elegido, on="date", how="left", coalesce=True)
    df_evolution_capital = df_evolution_capital.fill_null(strategy="forward")

    # Grafica
    fig = go.Figure()

    # Portafolio Trace
    fig.add_trace(go.Scatter(
        x=df_evolution_capital["date"],
        y=df_evolution_capital["Monto_ini"],
        mode='lines',
        name='Portafolio',
        line=dict(color='#ab63fa')
    ))
    
    # Logic for tooltip formatting
    color_up = colores_hex['up']
    color_down = colores_hex['down']

    def format_stat(val, is_pct=False):
        color = color_up if val >= 0 else color_down
        symbol = "▲" if val >= 0 else "▼"
        txt = f"{val:,.2f}"
        if is_pct: txt += "%"
        return f"<span style='color:{color}'>{symbol} {txt}</span>"

    profit_formatted = format_stat(profit_tooltip, is_pct=True)
    ganancia_formatted = format_stat(ganancia_tooltip)
    proj_formatted = format_stat(proyeccion_anual_tooltip, is_pct=True)
    drop_value_formatted = f"<span style='color:{colores_hex['modelo_elegido']}; font-size: 12px'>{drop_value}</span>"
    
    # Info Data for Annotation (White text wrapper)
    info_text = (
        f"<span style='color:white; font-size: 12px'>"
        f"<b>{drop_value_formatted}</b><br>" 
        f"Dias: {dias}<br>" 
        f"Trades: {trades_tooltip}<br>" 
        f"Aciertos: {aciertos_tooltip}<br>" 
        f"Winrate: {winrate_tooltip}%<br>" 
        f"Ganancia: {ganancia_formatted}<br>"  
        f"Profit %: {profit_formatted}<br>" 
        f"Proyección Anual: {proj_formatted}"
        f"</span>"
    )

    fig.add_trace(go.Scatter(
        x=df_evolution_capital["date"],
        y=df_evolution_capital[drop_value],
        mode='lines',
        name=drop_value,
        line=dict(color=colores_hex["modelo_elegido"])
    ))

    fig.update_layout(
        title={
            'text': titulo_grafica,
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
            bgcolor='rgba(0,0,0,0)',
            # Ensure legend is TO THE RIGHT of the plot
            y=1,
            x=1.05,
            xanchor='left', # Anchor left so it expands to the right from 1.05
            yanchor='top'
        ),
        # Add annotation below legend
        annotations=[
            dict(
                x=1.05,
                y=0.8, # Positioned below the legend
                xref="paper",
                yref="paper",
                text=info_text,
                showarrow=False,
                align="left",
                xanchor='left', # Anchor left to align with legend
                yanchor='top',
                bgcolor="rgba(0,0,0,0)"
            )
        ],
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
        # Increase right margin to make room for legend/annotation
        margin=dict(l=20, r=200, t=40, b=20),
        # Removed hovermode="x unified" to restore default tooltip behavior 
    )

    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        style={'height': '100%', 'width': '100%'}
    )

    