import polars as pl
from dash import html
from utils.utils import colores_hex



def returned_component_performance(df_back_spx: pl.DataFrame, df_back_eur: pl.DataFrame, df_back_btc: pl.DataFrame, df_back_xau: pl.DataFrame) -> html.Div:
    
    monto_portafolio = df_back_btc["Monto_fin_dia"][-1] + df_back_eur["Monto_fin_dia"][-1] \
                       + df_back_xau["Monto_fin_dia"][-1] + df_back_spx["Monto_fin_dia"][-1]                   
    monto_inicial = df_back_btc["Monto_ini_dia"][0] + df_back_eur["Monto_ini_dia"][0] + df_back_spx["Monto_ini_dia"][0] + df_back_xau["Monto_ini_dia"][0]
    
    variacion_portafolio = round(((monto_portafolio - monto_inicial) / monto_inicial * 100), 2)
    dias_operados = len(df_back_btc)    
    
    total_operaciones = df_back_btc["operaciones"].sum() + df_back_eur["operaciones"].sum() + df_back_xau["operaciones"].sum() + df_back_spx["operaciones"].sum()
    total_aciertos = df_back_btc["aciertos"].sum() + df_back_eur["aciertos"].sum() + df_back_xau["aciertos"].sum() + df_back_spx["aciertos"].sum()
    winrate_portafolio = round((total_aciertos / total_operaciones * 100),2)  if total_operaciones > 0 else 0

    proyeccion_anual = round((variacion_portafolio / dias_operados * 365), 2)

    # Lógica de colores y símbolos
    color_profit = colores_hex["up"] if variacion_portafolio > 0 else colores_hex["down"]
    simbolo_profit = '▲' if variacion_portafolio > 0 else '▼'

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
            html.Span(f"{winrate_portafolio}%", style={'fontSize': '1.3rem', 'fontWeight': 'bold'})
        ], style={'color': '#719CC6'}),
        html.Div(f"Trades {total_operaciones}", style={'fontSize': '0.9rem', 'fontWeight': 'bold', 'color': 'white'})
    ], style=estilo_bloque)

    # Bloque 2: Profit & Days
    bloque_2 = html.Div([
        html.Div([
            html.Span("Profit% ", style={'fontSize': '1.1rem', 'fontWeight': 'bold', 'color': 'white'}),
            html.Span(f"{simbolo_profit} {variacion_portafolio}%", style={'fontSize': '1.3rem', 'fontWeight': 'bold', 'color': color_profit})
        ]),
        # html.Div(f"Dias {dias_operados}", style={'fontSize': '0.9rem', 'color': '#8F9BA3'})
        html.Div(f"Dias {dias_operados}", style={'fontSize': '0.9rem', 'fontWeight': 'bold', 'color': 'white'})
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
