from dash import Input, Output, callback
import polars as pl
import numpy as np
from datetime import datetime, timezone
from functions.obtener_data_github import obtener_data_github
from functions.pasar_data_de_instrumentos_a_librerias import pasar_data_de_instrumentos_a_librerias
from functions.backtesting_instrumentos import backtesting_btcusd, backtesting_eurusd, backtesting_xauusd, backtesting_spx
from functions.backtesting_librerias import backtesting_librerias
from functions.backtesting_instrumentos_por_libreria import backtesting_btcusd_x_libreria, backtesting_eurusd_x_libreria
from functions.backtesting_instrumentos_por_libreria import backtesting_xauusd_x_libreria, backtesting_spx_x_libreria
from functions.backtesting_portafolio import backtesting_portafolio
from utils.utils import paths_data_github, paths_data_por_libreria

inicio_operaciones = datetime(2025, 8, 1).date()
hoy = datetime.now(timezone.utc).date()


def realizar_backtesting_instrumentos(df_btcusd: pl.DataFrame, df_eurusd: pl.DataFrame, df_xauusd: pl.DataFrame,
                                      df_spx: pl.DataFrame, datos: dict) -> dict:
    df_back_btc = backtesting_btcusd(df=df_btcusd)
    df_back_eur = backtesting_eurusd(df=df_eurusd)
    df_back_spx = backtesting_spx(df=df_spx)
    df_back_xau = backtesting_xauusd(df=df_xauusd)

    datos["back_btc"] = df_back_btc.to_dicts()
    datos["back_eur"] = df_back_eur.to_dicts()
    datos["back_xau"] = df_back_xau.to_dicts()
    datos["back_spx"] = df_back_spx.to_dicts()

    # Evolucion del Capital
    btc_evolution_capital = df_back_btc.select(["date", "Monto_ini_dia"])
    btc_evolution_capital.columns = ["date", "BTCUSD"]

    eur_evolution_capital = df_back_eur.select(["date", "Monto_ini_dia"])
    eur_evolution_capital.columns = ["date", "EURUSD"]

    xau_evolution_capital = df_back_xau.select(["date", "Monto_ini_dia"])
    xau_evolution_capital.columns = ["date", "XAUUSD"]

    spx_evolution_capital = df_back_spx.select(["date", "Monto_ini_dia"])
    spx_evolution_capital.columns = ["date", "SPX"]

    df_evolution_capital = btc_evolution_capital.join(eur_evolution_capital, on="date", how="left", coalesce=True )
    df_evolution_capital = df_evolution_capital.join(xau_evolution_capital, on="date", how="left", coalesce=True)
    df_evolution_capital = df_evolution_capital.join(spx_evolution_capital, on="date", how="left", coalesce=True)

    df_evolution_capital = df_evolution_capital.fill_null(strategy="forward")
    df_evolution_capital = df_evolution_capital.with_columns(
        pl.sum_horizontal(["BTCUSD", "EURUSD", "XAUUSD", "SPX"]).alias("Portafolio")
    )
    datos["evolution_capital"] = df_evolution_capital.to_dicts()

    # Operaciones, Aciertos y WinRates
    operaciones_btc = df_back_btc["operaciones"].sum()
    aciertos_btc = df_back_btc["aciertos"].sum()
    winrate_btc = round((aciertos_btc / operaciones_btc * 100),2)  if operaciones_btc > 0 else 0   

    operaciones_eur = df_back_eur["operaciones"].sum()  
    aciertos_eur = df_back_eur["aciertos"].sum()
    winrate_eur = round((aciertos_eur / operaciones_eur * 100),2)  if operaciones_eur > 0 else 0 

    operaciones_xau = df_back_xau["operaciones"].sum()
    aciertos_xau = df_back_xau["aciertos"].sum()
    winrate_xau = round((aciertos_xau / operaciones_xau * 100),2)  if operaciones_xau > 0 else 0

    operaciones_spx = df_back_spx["operaciones"].sum()
    aciertos_spx = df_back_spx["aciertos"].sum()
    winrate_spx = round((aciertos_spx / operaciones_spx * 100),2)  if operaciones_spx > 0 else 0

    operaciones_portafolio = operaciones_btc + operaciones_eur + operaciones_xau + operaciones_spx
    aciertos_portafolio = aciertos_btc + aciertos_eur + aciertos_xau + aciertos_spx
    winrate_portafolio = round((aciertos_portafolio / operaciones_portafolio * 100),2)  if operaciones_portafolio > 0 else 0

    data = {
        "Instrumento": ["S&P 500", "EURUSD", "BTCUSD","XAUUSD", "PORTAFOLIO"],
        "Operaciones": [operaciones_spx, operaciones_eur, operaciones_btc, operaciones_xau, operaciones_portafolio],
        "Aciertos": [aciertos_spx, aciertos_eur, aciertos_btc, aciertos_xau, aciertos_portafolio],
        "Winrate": [winrate_spx, winrate_eur, winrate_btc, winrate_xau, winrate_portafolio] 
    }    
    df_summary_winrate = pl.DataFrame(data)
    datos["summary_winrate"] = df_summary_winrate.to_dicts()

    return datos


def realizar_backtesting_instrumentos_por_libreria(df_btcusd: pl.DataFrame, df_eurusd: pl.DataFrame, df_xauusd: pl.DataFrame,
                                                   df_spx: pl.DataFrame, datos: dict) -> dict:
    df_back_btc_sklearn = backtesting_btcusd_x_libreria(df=df_btcusd, libreria="sklearn")
    df_back_btc_lightgbm = backtesting_btcusd_x_libreria(df=df_btcusd, libreria="lightgbm")
    df_back_btc_xgboost = backtesting_btcusd_x_libreria(df=df_btcusd, libreria="xgboost")
    df_back_btc_pytorch = backtesting_btcusd_x_libreria(df=df_btcusd, libreria="pytorch")
    df_back_btc_tensorflow = backtesting_btcusd_x_libreria(df=df_btcusd, libreria="tensorflow")

    datos["df_back_btc_sklearn"] = df_back_btc_sklearn.to_dicts()
    datos["df_back_btc_lightgbm"] = df_back_btc_lightgbm.to_dicts()
    datos["df_back_btc_xgboost"] = df_back_btc_xgboost.to_dicts()
    datos["df_back_btc_pytorch"] = df_back_btc_pytorch.to_dicts()
    datos["df_back_btc_tensorflow"] = df_back_btc_tensorflow.to_dicts()

    df_back_eur_sklearn = backtesting_eurusd_x_libreria(df=df_eurusd, libreria="sklearn")
    df_back_eur_lightgbm = backtesting_eurusd_x_libreria(df=df_eurusd, libreria="lightgbm")
    df_back_eur_xgboost = backtesting_eurusd_x_libreria(df=df_eurusd, libreria="xgboost")
    df_back_eur_pytorch = backtesting_eurusd_x_libreria(df=df_eurusd, libreria="pytorch")
    df_back_eur_tensorflow = backtesting_eurusd_x_libreria(df=df_eurusd, libreria="tensorflow")

    datos["df_back_eur_sklearn"] = df_back_eur_sklearn.to_dicts()
    datos["df_back_eur_lightgbm"] = df_back_eur_lightgbm.to_dicts()
    datos["df_back_eur_xgboost"] = df_back_eur_xgboost.to_dicts()
    datos["df_back_eur_pytorch"] = df_back_eur_pytorch.to_dicts()
    datos["df_back_eur_tensorflow"] = df_back_eur_tensorflow.to_dicts()

    df_back_xau_sklearn = backtesting_xauusd_x_libreria(df=df_xauusd, libreria="sklearn")
    df_back_xau_lightgbm = backtesting_xauusd_x_libreria(df=df_xauusd, libreria="lightgbm")
    df_back_xau_xgboost = backtesting_xauusd_x_libreria(df=df_xauusd, libreria="xgboost")
    df_back_xau_pytorch = backtesting_xauusd_x_libreria(df=df_xauusd, libreria="pytorch")
    df_back_xau_tensorflow = backtesting_xauusd_x_libreria(df=df_xauusd, libreria="tensorflow")

    datos["df_back_xau_sklearn"] = df_back_xau_sklearn.to_dicts()
    datos["df_back_xau_lightgbm"] = df_back_xau_lightgbm.to_dicts()
    datos["df_back_xau_xgboost"] = df_back_xau_xgboost.to_dicts()
    datos["df_back_xau_pytorch"] = df_back_xau_pytorch.to_dicts()
    datos["df_back_xau_tensorflow"] = df_back_xau_tensorflow.to_dicts()

    df_back_spx_sklearn = backtesting_spx_x_libreria(df=df_spx, libreria="sklearn")
    df_back_spx_lightgbm = backtesting_spx_x_libreria(df=df_spx, libreria="lightgbm")
    df_back_spx_xgboost = backtesting_spx_x_libreria(df=df_spx, libreria="xgboost")
    df_back_spx_pytorch = backtesting_spx_x_libreria(df=df_spx, libreria="pytorch")
    df_back_spx_tensorflow = backtesting_spx_x_libreria(df=df_spx, libreria="tensorflow")

    datos["df_back_spx_sklearn"] = df_back_spx_sklearn.to_dicts()
    datos["df_back_spx_lightgbm"] = df_back_spx_lightgbm.to_dicts()
    datos["df_back_spx_xgboost"] = df_back_spx_xgboost.to_dicts()
    datos["df_back_spx_pytorch"] = df_back_spx_pytorch.to_dicts()
    datos["df_back_spx_tensorflow"] = df_back_spx_tensorflow.to_dicts()

    return datos


def realizar_backtesting_librerias(df_sklearn: pl.DataFrame, df_lightgbm: pl.DataFrame, df_xgboost: pl.DataFrame,
                                   df_pytorch: pl.DataFrame, df_tensorflow: pl.DataFrame, datos: dict) -> dict:
    df_back_sklearn = backtesting_librerias(df=df_sklearn)
    df_back_lightgbm = backtesting_librerias(df=df_lightgbm)
    df_back_xgboost = backtesting_librerias(df=df_xgboost)
    df_back_pytorch = backtesting_librerias(df=df_pytorch)
    df_back_tensorflow = backtesting_librerias(df=df_tensorflow)

    datos["df_back_sklearn"] = df_back_sklearn.to_dicts()
    datos["df_back_lightgbm"] = df_back_lightgbm.to_dicts()
    datos["df_back_xgboost"] = df_back_xgboost.to_dicts()
    datos["df_back_pytorch"] = df_back_pytorch.to_dicts()
    datos["df_back_tensorflow"] = df_back_tensorflow.to_dicts()

    return datos


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
    # pasar_data_de_instrumentos_a_librerias()
    datos = {}

    df_btcusd = pl.read_parquet(paths_data_github["BTCUSD"])
    df_eurusd = pl.read_parquet(paths_data_github["EURUSD"])
    df_xauusd = pl.read_parquet(paths_data_github["XAUUSD"])
    df_spx = pl.read_parquet(paths_data_github["SPX"])

    df_sklearn = pl.read_parquet(paths_data_por_libreria["sklearn"])
    df_lightgbm = pl.read_parquet(paths_data_por_libreria["lightgbm"])
    df_xgboost = pl.read_parquet(paths_data_por_libreria["xgboost"])
    df_pytorch = pl.read_parquet(paths_data_por_libreria["pytorch"])
    df_tensorflow = pl.read_parquet(paths_data_por_libreria["tensorflow"])

    datos["btcusd"] = df_btcusd.to_dicts()
    datos["eurusd"] = df_eurusd.to_dicts()
    datos["xauusd"] = df_xauusd.to_dicts()
    datos["spx"] = df_spx.to_dicts()
    datos["sklearn"] = df_sklearn.to_dicts()
    datos["lightgbm"] = df_lightgbm.to_dicts()
    datos["xgboost"] = df_xgboost.to_dicts()
    datos["pytorch"] = df_pytorch.to_dicts()
    datos["tensorflow"] = df_tensorflow.to_dicts()

    datos = realizar_backtesting_instrumentos(df_btcusd=df_btcusd, df_eurusd=df_eurusd, df_xauusd=df_xauusd, df_spx=df_spx, datos=datos)
    datos = realizar_backtesting_librerias(df_sklearn=df_sklearn, df_lightgbm=df_lightgbm, df_xgboost=df_xgboost,
                                           df_pytorch=df_pytorch, df_tensorflow=df_tensorflow, datos=datos)
    datos = realizar_backtesting_instrumentos_por_libreria(df_btcusd=df_btcusd, df_eurusd=df_eurusd, df_xauusd=df_xauusd, df_spx=df_spx, datos=datos)
    df_portafolio = backtesting_portafolio(df_sklearn=df_sklearn, df_lightgbm=df_lightgbm, df_xgboost=df_xgboost,
                                           df_pytorch=df_pytorch, df_tensorflow=df_tensorflow)

    datos["portafolio"] = df_portafolio.to_dicts()
    datos["fecha_ini"] = inicio_operaciones
    datos["fecha_fin"] = hoy
    return datos
