from dash import dcc
import plotly.graph_objects as go
import polars as pl
from utils.utils import colores_hex

def returned_tabla_gde_instrumentos(df_trades_aciertos_diarios: pl.DataFrame):
    df = df_trades_aciertos_diarios.select(["date", "Trades-SP-500", "✅-SP-500", "Trades-EUR", "✅-EUR", "Trades-BTC", "✅-BTC", "Trades-XAU", "✅-XAU"])
    df = df.rename({"date": "Fecha"})
    
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

    # Equal width for all columns. Date was taking too much space, this forces equality.
    # We can adjust ratios if needed (e.g., date=1, others=1).
    fig.update_traces(columnwidth=[1]*len(df.columns))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )
    
    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        style={'height': '95%', 'width': '98%'}
    )
    