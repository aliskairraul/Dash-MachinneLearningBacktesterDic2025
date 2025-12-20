from dash import dcc
import plotly.graph_objects as go
import polars as pl
from utils.utils import colores_hex

def returned_tabla_gde_elegido(df_trades_aciertos: pl.DataFrame, df_elegido: pl.DataFrame, nombre_elegido: str):
    df_elegido = df_elegido.select(["date", "operaciones", "aciertos"]) 
    df_elegido.columns = ["date", f"Trades-{nombre_elegido}", f"✅-{nombre_elegido}"]
    df = df_trades_aciertos.select(["date", "Trades_Portafolio", "✅_Portafolio"])
    df = df.join(df_elegido, on="date", how="left", coalesce=True)
    df = df.fill_null(strategy="forward")
    df = df.rename({"date": "Fecha"})
    
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
    