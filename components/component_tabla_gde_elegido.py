from dash import dcc
import plotly.graph_objects as go
import polars as pl
from utils.utils import colores_hex

def returned_tabla_gde_elegido(df_trades: pl.DataFrame, df_elegido: pl.DataFrame, nombre_elegido: str, estrategia: str) -> dcc.Graph:
    df = pl.DataFrame()
    if estrategia == "Individual":
        df = df_trades.select(["date", "Portafolio Trades", "Portafolio Wins"]) 
    else:
        df = df_trades.select(["date", "Portafolio Trades Mayoria", "Portafolio Wins Mayoria"])

    df.columns = ["date", "Trades_Portafolio", "✅_Portafolio"]

    df_elegido = df_elegido.select(["date", "trades_dia", "wins_dia"]) 
    df_elegido.columns = ["date", f"Trades-{nombre_elegido}", f"✅-{nombre_elegido}"]

    df = df.join(df_elegido, on="date", how="left", coalesce=True)
    df = df.fill_null(strategy="zero")
    df = df.rename({"date": "Fecha"}).sort("Fecha", descending=True)
    
    cells_colors = []
    for col in df.columns:
        if nombre_elegido in col:
            cells_colors.append(colores_hex['modelo_elegido'])
        elif "Portafolio" in col:
            cells_colors.append(colores_hex['portafolio'])
        else:
            cells_colors.append("#D6D1D0")

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(df.columns),
            fill_color='#374352',
            align='center',
            font=dict(color='white', size=10)
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            # fill_color='white',
            fill_color=cells_colors,
            align='center',
            font=dict(color='black', size=11),
            height=30
        )
    )])

    fig.update_traces(columnwidth=[1]*len(df.columns))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )
    
    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        style={'height': '95%', 'width': '98%'}
    )
    