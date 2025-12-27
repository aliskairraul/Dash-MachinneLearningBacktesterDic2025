from dash import Input, Output, callback
import polars as pl
import numpy as np
from datetime import datetime, timezone
from functions.obtener_data_github import obtener_data_github
from functions.backtesting import backtesting_btcusd, backtesting_eurusd, backtesting_spx, backtesting_xauusd, backtesting_especifico, trades
from utils.utils import paths_inferencias

inicio_operaciones = datetime(2025, 8, 1).date()
hoy = datetime.now(timezone.utc).date()


@callback(
    Output("store-ready", "data"),
    Input("store-datos", "data"),
)
def marcar_datos_listos(datos):
    '''FUNCION ESTRATEGIA PARA QUE NO SE INTENTE "actualizar_componentes" SI LA DATA NECESARIA NO SE HA CARGADO Y TRANSFORMADO '''
    return bool(datos)


# 🪟 Callback para cerrar el modal cuando la data esté lista
@callback(
    Output("modal-loading", "is_open"),
    Input("store-datos", "data"),
    prevent_initial_call=True
)
def cerrar_modal(data):
    '''CERRANDO MODAL CUANDO SE CARGA LA DATA AL INICIO'''
    return False if data else True


# 🧠 Callback para cargar la data
@callback(
    Output("store-datos", "data"),
    Input("interval-loader", "n_intervals"),
    prevent_initial_call=True
)
def cargar_data(n):
    # obtener_data_github()
    datos = {}

    inferencias_btc = pl.read_parquet(paths_inferencias["BTCUSD"])
    back_btc_individual = backtesting_btcusd(df=inferencias_btc, estrategia="INDIVIDUAL")
    back_btc_ponderada = backtesting_btcusd(df=inferencias_btc, estrategia="MAYORIA_PONDERADA")
    back_btc_estricta = backtesting_btcusd(df=inferencias_btc, estrategia="MAYORIA_ESTRICTA")

    datos["back_btc_individual"] = back_btc_individual.to_dicts()
    datos["back_btc_ponderada"] = back_btc_ponderada.to_dicts()
    datos["back_btc_estricta"] = back_btc_estricta.to_dicts()

    inferencias_eur = pl.read_parquet(paths_inferencias["EURUSD"])
    back_eur_individual = backtesting_eurusd(df=inferencias_eur, estrategia="INDIVIDUAL")
    back_eur_ponderada = backtesting_eurusd(df=inferencias_eur, estrategia="MAYORIA_PONDERADA")
    back_eur_estricta = backtesting_eurusd(df=inferencias_eur, estrategia="MAYORIA_ESTRICTA")

    datos["back_eur_individual"] = back_eur_individual.to_dicts()
    datos["back_eur_ponderada"] = back_eur_ponderada.to_dicts()
    datos["back_eur_estricta"] = back_eur_estricta.to_dicts()

    inferencias_xau = pl.read_parquet(paths_inferencias["XAUUSD"])
    back_xau_individual = backtesting_xauusd(df=inferencias_xau, estrategia="INDIVIDUAL")
    back_xau_ponderada = backtesting_xauusd(df=inferencias_xau, estrategia="MAYORIA_PONDERADA")
    back_xau_estricta = backtesting_xauusd(df=inferencias_xau, estrategia="MAYORIA_ESTRICTA")

    datos["back_xau_individual"] = back_xau_individual.to_dicts()
    datos["back_xau_ponderada"] = back_xau_ponderada.to_dicts()
    datos["back_xau_estricta"] = back_xau_estricta.to_dicts()

    inferencias_spx = pl.read_parquet(paths_inferencias["SPX"])
    back_spx_individual = backtesting_spx(df=inferencias_spx, estrategia="INDIVIDUAL")
    back_spx_ponderada = backtesting_spx(df=inferencias_spx, estrategia="MAYORIA_PONDERADA")
    back_spx_estricta = backtesting_spx(df=inferencias_spx, estrategia="MAYORIA_ESTRICTA")

    datos["back_spx_individual"] = back_spx_individual.to_dicts()
    datos["back_spx_ponderada"] = back_spx_ponderada.to_dicts()
    datos["back_spx_estricta"] = back_spx_estricta.to_dicts()

    # Combinaciones específicas de Librerias/instrumentos
    librerias = ["sklearn", "lightgbm", "xgboost", "pytorch", "tensorflow"]
    symbol_corto = ["btc", "eur", "spx", "xau"]
    instrumentos = ["btcusd", "eurusd", "spxusd", "xauusd"]
    inferencias = [inferencias_btc, inferencias_eur, inferencias_spx, inferencias_xau]
    backs_especificos = {}
    for i, instrumento in enumerate(instrumentos):
        for libreria in librerias:
            df = backtesting_especifico(df=inferencias[i], libreria=libreria, instrumento=instrumento)
            if df.shape[0] > 0:
                backs_especificos[f"back_{symbol_corto[i]}_{libreria}"] = df

    lista_keys = list(backs_especificos.keys())
    for symbol in symbol_corto:
        for libreria in librerias:
            key = f"back_{symbol}_{libreria}"
            if key not in lista_keys:
                continue
            datos[key] = backs_especificos[key].to_dicts()

    df_trades = trades(inferencias_btc=inferencias_btc, inferencias_eur=inferencias_eur, inferencias_spx=inferencias_spx, inferencias_xau=inferencias_xau)
    datos["df_trades"] = df_trades.to_dicts()

    lista_keys = list(datos.keys())
    datos["lista_reconvertir_dates"] = lista_keys
    datos["fecha_ini"] = inicio_operaciones
    datos["fecha_fin"] = hoy
    return datos
