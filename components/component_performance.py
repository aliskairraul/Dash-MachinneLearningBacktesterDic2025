import polars as pl
from dash import html
from functions.backtesting import evolucion
from utils.utils import colores_hex



def returned_component_performance(df_spx: pl.DataFrame, df_eur: pl.DataFrame, df_btc: pl.DataFrame,
                                   df_xau: pl.DataFrame, df_trades: pl.DataFrame, estrategia: str) -> html.Div:
    df_evolucion = evolucion(df_spx=df_spx, df_eur=df_eur, df_btc=df_btc, df_xau=df_xau)
    dias = df_evolucion.shape[0]
    profit = round(((df_evolucion["Monto_fin"][-1] - df_evolucion["Monto_ini"][0]) / df_evolucion["Monto_ini"][0] * 100), 2)
    proyeccion_anual = round(profit * 365 / dias, 2)

    trades = df_trades["Portafolio Trades"].sum() if estrategia == "Individual" else df_trades["Portafolio Trades Mayoria"].sum() 
    wins = df_trades["Portafolio Wins"].sum() if estrategia == "Individual" else df_trades["Portafolio Wins Mayoria"].sum()

    winrate = round((wins / trades * 100), 2) if trades > 0 else 0

    # Lógica de colores y símbolos
    color_profit = colores_hex["up"] if profit > 0 else colores_hex["down"]
    simbolo_profit = '▲' if profit > 0 else '▼'

    # Estilos comunes
    estilo_bloque = {
        'padding': '10px',
        'borderBottom': '1px solid #2C3E50',
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',
        'alignItems': 'flex-start'
    }

    # Bloque 1: Win Rate & Trades
    bloque_1 = html.Div([
        html.Div([
            html.Span("Win Rate ", style={'fontSize': '1.1rem', 'fontWeight': 'bold'}),
            html.Span(f"{winrate}%", style={'fontSize': '1.3rem', 'fontWeight': 'bold'})
        ], style={'color': '#719CC6'}),
        html.Div(f"Trades {trades}", style={'fontSize': '0.9rem', 'fontWeight': 'bold', 'color': 'white'})
    ], style=estilo_bloque)

    # Bloque 2: Profit & Days
    bloque_2 = html.Div([
        html.Div([
            html.Span("Profit% ", style={'fontSize': '1.1rem', 'fontWeight': 'bold', 'color': 'white'}),
            html.Span(f"{simbolo_profit} {profit}%", style={'fontSize': '1.3rem', 'fontWeight': 'bold', 'color': color_profit})
        ]),
        # html.Div(f"Dias {dias_operados}", style={'fontSize': '0.9rem', 'color': '#8F9BA3'})
        html.Div(f"Dias {dias}", style={'fontSize': '0.9rem', 'fontWeight': 'bold', 'color': 'white'})
    ], style=estilo_bloque)

    # Bloque 3: Annual Projection
    bloque_3 = html.Div([
        # html.Span("Annual projection ", style={'fontSize': '1rem', 'color': '#8F9BA3'}),
        html.Span("Proyección Anual ", style={'fontSize': '1.1rem', 'fontWeight': 'bold', 'color': 'white'}),
        html.Span(f"{simbolo_profit} {proyeccion_anual}%", style={'fontSize': '1.1rem', 'fontWeight': 'bold', 'color': color_profit})
    ], style={**estilo_bloque, 'borderBottom': 'none', 'flexDirection': 'row', 'justifyContent': 'space-between', 'alignItems': 'center'})

    return html.Div([
        bloque_1,
        bloque_2,
        bloque_3
    ], style={'display': 'flex', 'flexDirection': 'column', 'height': '100%', 'justifyContent': 'space-around'})
