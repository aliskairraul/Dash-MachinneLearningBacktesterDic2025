import polars as pl
from dash import Dash, dcc, html, Input, Output, callback, exceptions, ctx
from datetime import datetime, timedelta
from components.component_drop import returned_drop_component
from components.component_cards import retorna_card
from components.component_dona_overview import returned_dona_overview
from components.component_current_equity import returned_current_equity
from components.component_performance import returned_component_performance
from components.component_barras_winrate import returned_barras_winrate
from components.component_tabla_trades import returned_tablas_trades
from components.component_evolucion_instrumentos import returned_evolucion_instrumentos
from components.component_evolucion_elegido import returned_evolucion_elegido
from utils.utils import keys_datos, diccionario_drop

def reconvirtiendo_datos(datos_serializados: dict, keys_datos: list, fecha_ini: datetime.date, fecha_fin: datetime.date) -> list:
    datos = {}
    for key in keys_datos:
        if key == "summary_winrate":
            df = pl.DataFrame(datos_serializados[key])
            datos[key] = df
            continue
        df = pl.DataFrame(datos_serializados[key]).with_columns(pl.col("date").cast(pl.Date))
        df = df.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))
        datos[key] = df
    return datos


def string_to_date(fecha_str: str) -> datetime.date:
    return datetime.strptime(fecha_str, "%Y-%m-%d").date()


@callback(
    Output("store-drop-value", "data"),
    Input("drop-down", "value"),
    prevent_initial_call=True
)
def actualizar_drop_value(drop_value):
    return drop_value


@callback(
    Output("area-drop", "children"),
    Output("grafico-portafolio-overview", "children"),
    Output("grafico-portafolio-evolucion", "children"),
    Output("portafolio-rates", "children"),
    Output("card-spx", "children"),
    Output("card-eur", "children"),
    Output("card-btc", "children"),
    Output("card-xau", "children"),
    Output("grafico-barras", "children"),
    Output("tabla-peq", "children"),
    Output("grafico-linechart", "children"),
    Output("store-primera-carga", "data"),
    Input("store-ready", "data"),
    Input("store-datos", "data"),
    Input("date-picker-single-ini", "date"),
    Input("date-picker-single-fin", "date"),
    Input("dcc-radioitems", "value"),
    Input("store-drop-value", "data"),
    Input("store-primera-carga", "data"),
    prevent_initial_call=True
)
def actualizar_componentes(store_ready, datos_serializados, fecha_ini_entrada, fecha_fin_entrada, radioitems_value, drop_value, es_primera_carga):
# def actualizar_componentes(store_ready, datos, es_primera_carga):
    if not store_ready:
        raise exceptions.PreventUpdate

    activado_por_drop = False    
    trigger_id = ctx.triggered_id
    if trigger_id == "store-drop-value":
        activado_por_drop = True

    disabled_drop_dow = False if radioitems_value == "opcion_drop" else True

    componente_drop = returned_drop_component(deactive_tab=disabled_drop_dow)

    fecha_ini = string_to_date(datos_serializados["fecha_ini"]) if es_primera_carga else string_to_date(fecha_ini_entrada)
    fecha_fin = string_to_date(datos_serializados["fecha_fin"]) if es_primera_carga else string_to_date(fecha_fin_entrada)
    
    datos = reconvirtiendo_datos(datos_serializados=datos_serializados, keys_datos=keys_datos, fecha_ini=fecha_ini, fecha_fin=fecha_fin)   

    card_spx = retorna_card(df=datos["back_spx"])   
    card_eur = retorna_card(df=datos["back_eur"])   
    card_btc = retorna_card(df=datos["back_btc"])   
    card_xau = retorna_card(df=datos["back_xau"])                                                                            
    
    dona_overview = returned_dona_overview(df_back_spx=datos["back_spx"], df_back_eur=datos["back_eur"],
                                           df_back_btc=datos["back_btc"], df_back_xau=datos["back_xau"])
        
    component_current_equity = returned_current_equity(df_evolution_capital=datos["evolution_capital"])
                                                       
    component_performance = returned_component_performance(df_back_spx=datos["back_spx"], df_back_eur=datos["back_eur"],
                                                           df_back_btc=datos["back_btc"], df_back_xau=datos["back_xau"])
    
    componente_barras = returned_barras_winrate(df_summary_winrate=datos["summary_winrate"])
    
    componente_tabla = returned_tablas_trades(df_summary_winrate=datos["summary_winrate"])
    
    componente_evolucion = returned_evolucion_instrumentos(df_evolution_capital=datos["evolution_capital"]) if not activado_por_drop else                           returned_evolucion_elegido(df_evolution_capital=datos["evolution_capital"], df_elegido=datos[diccionario_drop[drop_value]], drop_value=drop_value)

    es_primera_carga = False
    return componente_drop, dona_overview, component_current_equity, component_performance, card_spx, card_eur, card_btc,\
           card_xau, componente_barras, componente_tabla, componente_evolucion, es_primera_carga