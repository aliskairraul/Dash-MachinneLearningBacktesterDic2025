import polars as pl
from dash import Dash, dcc, html, Input, Output, callback, exceptions, ctx, no_update
from datetime import datetime, timedelta
from components.component_drop import returned_drop_component
from components.component_cards import retorna_card
from components.component_dona_overview import returned_dona_overview
from components.component_evolucion_patrimonio import returned_evolucion_patrimonio
from components.component_performance import returned_component_performance
from components.component_barras_winrate import returned_barras_winrate
from components.component_tabla_trades import returned_tablas_trades
from components.component_evolucion_instrumentos import returned_evolucion_instrumentos
from components.component_evolucion_elegido import returned_evolucion_elegido
from utils.utils import diccionario_drop
from components.component_tabla_gde_instrumentos import returned_tabla_gde_instrumentos
from components.component_tabla_gde_elegido import returned_tabla_gde_elegido

def reconvirtiendo_dates(datos_serializados: dict, fecha_ini: datetime.date, fecha_fin: datetime.date) -> list:
    datos = {}
    for key in datos_serializados.keys():
        if key not in datos_serializados["lista_reconvertir_dates"]:
            datos[key] = datos_serializados[key]
            continue
        
        df = pl.DataFrame(datos_serializados[key]).with_columns(pl.col("date").cast(pl.Date))
        df = df.filter((pl.col("date") >= fecha_ini) & (pl.col("date") <= fecha_fin))
        datos[key] = df
    return datos


def string_to_date(fecha_str: str) -> datetime.date:
    return datetime.strptime(fecha_str, "%Y-%m-%d").date()


@callback(
    Output("modal-error-fechas", "is_open", allow_duplicate=True),
    Input("btn-cerrar-modal-error", "n_clicks"),
    prevent_initial_call=True
)
def cerrar_modal_error(n_clicks):
    if n_clicks:
        return False
    return no_update


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
    Output("tabla-gde", "children"),
    Output("store-primera-carga", "data"),
    Output("modal-error-fechas", "is_open"),
    Input("store-ready", "data"),
    Input("store-datos", "data"),
    Input("date-picker-single-ini", "date"),
    Input("date-picker-single-fin", "date"),
    Input("dcc-radioitems", "value"),
    Input("drop-estrategias", "value"),
    Input("store-drop-value", "data"),
    Input("store-primera-carga", "data"),
    prevent_initial_call=True
)
def actualizar_componentes(store_ready, datos_serializados, fecha_ini_entrada, fecha_fin_entrada,
                           radioitems_value, estrategia, drop_value, es_primera_carga):
    if not store_ready:
        raise exceptions.PreventUpdate

    if string_to_date(fecha_fin_entrada) <= string_to_date(fecha_ini_entrada):
        return [no_update] * 13 + [True]

    activado_por_drop = False    
    trigger_id = ctx.triggered_id
    if (trigger_id == "store-drop-value" and drop_value) or (radioitems_value == "opcion_drop" and drop_value):
        activado_por_drop = True 

    disabled_drop_dow = False if radioitems_value == "opcion_drop" else True
    value_drop = drop_value if not es_primera_carga else None
    componente_drop = returned_drop_component(deactive_tab=disabled_drop_dow, value_drop=value_drop)

    fecha_ini = string_to_date(datos_serializados["fecha_ini"]) if es_primera_carga else string_to_date(fecha_ini_entrada)
    fecha_fin = string_to_date(datos_serializados["fecha_fin"]) if es_primera_carga else string_to_date(fecha_fin_entrada)
    
    datos = reconvirtiendo_dates(datos_serializados=datos_serializados, fecha_ini=fecha_ini, fecha_fin=fecha_fin) 

    if estrategia == "Individual":
        back_spx = datos["back_spx_individual"]
        back_eur = datos["back_eur_individual"]
        back_btc = datos["back_btc_individual"]
        back_xau = datos["back_xau_individual"]
    elif estrategia == "Mayoria Ponderada":
        back_spx = datos["back_spx_ponderada"]
        back_eur = datos["back_eur_ponderada"]
        back_btc = datos["back_btc_ponderada"]
        back_xau = datos["back_xau_ponderada"]
    else:
        back_spx = datos["back_spx_estricta"]
        back_eur = datos["back_eur_estricta"]
        back_btc = datos["back_btc_estricta"]
        back_xau = datos["back_xau_estricta"]


    card_spx = retorna_card(df=back_spx, habiles_anio=252)   
    card_eur = retorna_card(df=back_eur, habiles_anio=252)   
    card_btc = retorna_card(df=back_btc, habiles_anio=365)   
    card_xau = retorna_card(df=back_xau, habiles_anio=252)                                                                            
    
    dona_overview = returned_dona_overview(df_spx=back_spx, df_eur=back_eur,
                                           df_btc=back_btc, df_xau=back_xau)
        
    componente_evolucion_patrimonio = returned_evolucion_patrimonio(df_spx=back_spx, df_eur=back_eur, df_btc=back_btc, df_xau=back_xau)
                                                       
    componente_performance = returned_component_performance(df_spx=back_spx, df_eur=back_eur, df_btc=back_btc,
                                                            df_xau=back_xau, df_trades=datos["df_trades"], estrategia=estrategia)
    
    componente_barras = returned_barras_winrate(df_spx=back_spx, df_eur=back_eur, df_btc=back_btc, df_xau=back_xau)
    
    componente_tabla = returned_tablas_trades(df_trades=datos["df_trades"], estrategia=estrategia)
    
    componente_evolucion = None
    componente_tabla_gde = None
    if not activado_por_drop:
        componente_evolucion = returned_evolucion_instrumentos(df_spx=back_spx, df_eur=back_eur, df_btc=back_btc, df_xau=back_xau) 
        
        componente_tabla_gde = returned_tabla_gde_instrumentos(df_trades=datos["df_trades"], estrategia=estrategia)
    else:
        componente_evolucion = returned_evolucion_elegido(df_spx=back_spx, df_eur=back_eur, df_btc=back_btc, df_xau=back_xau,
                                                          df_elegido=datos[diccionario_drop[drop_value]], drop_value=drop_value)

        componente_tabla_gde = returned_tabla_gde_elegido(df_trades=datos["df_trades"], nombre_elegido=drop_value,
                                                          df_elegido=datos[diccionario_drop[drop_value]], estrategia=estrategia)
    
    es_primera_carga = False
    
    return componente_drop, dona_overview, componente_evolucion_patrimonio, componente_performance, card_spx, card_eur, card_btc, card_xau,\
           componente_barras, componente_tabla, componente_evolucion, componente_tabla_gde, es_primera_carga, False
