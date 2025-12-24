import polars as pl
from pathlib import Path
from datetime import date

urls_inferencias_predicciones = {
    "BTCUSD": "https://raw.githubusercontent.com/aliskairraul/Inferencias_instrumentos_dic_2025/main/data/inferencias/predicciones_aciertos_btcusd.parquet",
    'EURUSD': "https://raw.githubusercontent.com/aliskairraul/Inferencias_instrumentos_dic_2025/main/data/inferencias/predicciones_aciertos_eurusd.parquet",
    'SPX': "https://raw.githubusercontent.com/aliskairraul/Inferencias_instrumentos_dic_2025/main/data/inferencias/predicciones_aciertos_spx.parquet",
    'XAUUSD': "https://raw.githubusercontent.com/aliskairraul/Inferencias_instrumentos_dic_2025/main/data/inferencias/predicciones_aciertos_xauusd.parquet",
}

paths_inferencias = {
    "BTCUSD": Path("data/inferencias/predicciones_aciertos_btcusd.parquet"),
    "EURUSD": Path("data/inferencias/predicciones_aciertos_eurusd.parquet"),
    "SPX": Path("data/inferencias/predicciones_aciertos_spx.parquet"),
    "XAUUSD": Path("data/inferencias/predicciones_aciertos_xauusd.parquet")
}

diccionario_drop = {
    "S&P 500 solo Sklearn" : "back_spx_sklearn",
    "S&P 500 solo LightGbm" : "back_spx_lightgbm",
    "S&P 500 solo XgBoost" : "back_spx_xgboost",
    "S&P 500 solo PyTorch" : "back_spx_pytorch",
    "S&P 500 solo TensorFlow" : "back_spx_tensorflow",
    "EURUSD solo Sklearn" : "back_eur_sklearn",
    "EURUSD solo LightGbm" : "back_eur_lightgbm",
    "EURUSD solo XgBoost" : "back_eur_xgboost",
    "EURUSD solo PyTorch" : "back_eur_pytorch",
    "EURUSD solo TensorFlow" : "back_eur_tensorflow",
    "BTCUSD solo Sklearn" : "back_btc_sklearn",
    "BTCUSD solo LightGbm" : "back_btc_lightgbm",
    "BTCUSD solo XgBoost" : "back_btc_xgboost",
    "BTCUSD solo TensorFlow" : "back_btc_tensorflow",
    "XAUUSD solo LightGbm" : "back_xau_lightgbm",
    "XAUUSD solo XgBoost" : "back_xau_xgboost",
    "XAUUSD solo TensorFlow" : "back_xau_tensorflow",
}

colores_hex = {
    "eurusd": "#6ED180",
    "btcusd": "#ff8c00",
    "xauusd": "#fffa5c",
    "spx": "#54A6DC",
    "portafolio": "#ab63fa",
    "sklearn": "#2e8b57",
    "lightgbm": "#ff8c00",
    "xgboost": "#4169e1",
    "pytorch": "#3A0603",
    "tensorflow": "#ab63fa",
    "up": "#79CA7C",
    "down": "#FF0000",
    "modelo_elegido": "#946B63",
}

columnas_librerias = {
    "sklearn": ['date', 'close', 'close_tomorrow', 'sklearn', 'sklearn_estrategia', 'sklearn_trade', 'sklearn_win'],
    "lightgbm": ['date', 'close', 'close_tomorrow', 'lightgbm', 'lightgbm_estrategia', 'lightgbm_trade', 'lightgbm_win'],
    "xgboost": ['date', 'close', 'close_tomorrow', 'xgboost', 'xgboost_estrategia', 'xgboost_trade', 'xgboost_win'],
    "pytorch": ['date', 'close', 'close_tomorrow', 'pytorch', 'pytorch_estrategia', 'pytorch_trade', 'pytorch_win'],
    "tensorflow": ['date', 'close', 'close_tomorrow', 'tensorflow', 'tensorflow_estrategia', 'tensorflow_trade', 'tensorflow_win'],
}


def returned_summary_winrate(df_back_spx: pl.DataFrame, df_back_eur: pl.DataFrame, df_back_btc: pl.DataFrame, df_back_xau: pl.DataFrame):
    operaciones_btc = df_back_btc["operaciones"].sum()
    aciertos_btc = df_back_btc["aciertos"].sum()
    winrate_btc = round((aciertos_btc / operaciones_btc * 100), 2) if operaciones_btc > 0 else 0

    operaciones_eur = df_back_eur["operaciones"].sum()
    aciertos_eur = df_back_eur["aciertos"].sum()
    winrate_eur = round((aciertos_eur / operaciones_eur * 100), 2) if operaciones_eur > 0 else 0

    operaciones_xau = df_back_xau["operaciones"].sum()
    aciertos_xau = df_back_xau["aciertos"].sum()
    winrate_xau = round((aciertos_xau / operaciones_xau * 100), 2) if operaciones_xau > 0 else 0

    operaciones_spx = df_back_spx["operaciones"].sum()
    aciertos_spx = df_back_spx["aciertos"].sum()
    winrate_spx = round((aciertos_spx / operaciones_spx * 100), 2) if operaciones_spx > 0 else 0

    operaciones_portafolio = operaciones_btc + operaciones_eur + operaciones_xau + operaciones_spx
    aciertos_portafolio = aciertos_btc + aciertos_eur + aciertos_xau + aciertos_spx
    winrate_portafolio = round((aciertos_portafolio / operaciones_portafolio * 100), 2) if operaciones_portafolio > 0 else 0

    data = {
        "Instrumento": ["S&P 500", "EURUSD", "BTCUSD", "XAUUSD", "PORTAFOLIO"],
        "Operaciones": [operaciones_spx, operaciones_eur, operaciones_btc, operaciones_xau, operaciones_portafolio],
        "Aciertos": [aciertos_spx, aciertos_eur, aciertos_btc, aciertos_xau, aciertos_portafolio],
        "Winrate": [winrate_spx, winrate_eur, winrate_btc, winrate_xau, winrate_portafolio]
    }
    df_summary_winrate = pl.DataFrame(data)
    return df_summary_winrate
