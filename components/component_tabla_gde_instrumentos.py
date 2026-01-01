from dash import dcc
import plotly.graph_objects as go
import polars as pl
from datetime import datetime
from utils.utils import colores_hex

def returned_tabla_gde_instrumentos(df_trades: pl.DataFrame, estrategia: str, fecha_ini: datetime.date,
                                    fecha_fin: datetime.date) -> dcc.Graph:
    df_trades = df_trades.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))
    if estrategia == "Individual":
        df = df_trades.select(["date", "spx_trades", "spx_wins", "eur_trades", "eur_wins", "btc_trades", "btc_wins", "xau_trades", "xau_wins"])
    else:
        df = df_trades.select(["date", "spx_mayoria_trades", "spx_mayoria_wins", "eur_mayoria_trades", "eur_mayoria_wins", "btc_mayoria_trades", "btc_mayoria_wins", "xau_mayoria_trades", "xau_mayoria_wins"])
               
    df.columns = ["Fecha", "trades SP-500", "✅-SP-500", "trades EUR", "✅-EUR", "trades BTC", "✅-BTC", "trades XAU", "✅-XAU"]
    df = df.sort("Fecha", descending=True)

    cells_colors = []
    for col in df.columns:
        if "SP-500" in col:
            cells_colors.append(colores_hex['spx'])
        elif "EUR" in col:
            cells_colors.append(colores_hex['eurusd'])
        elif "BTC" in col:
            cells_colors.append(colores_hex['btcusd'])
        elif "XAU" in col:
            cells_colors.append(colores_hex['xauusd'])
        else:
            cells_colors.append('#D6D1D0')

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
    