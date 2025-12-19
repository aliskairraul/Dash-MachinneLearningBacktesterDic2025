import polars as pl
from pathlib import Path
from datetime import date

urls_inferencias_predicciones = {
    "BTCUSD": "https://raw.githubusercontent.com/aliskairraul/Inferencias_instrumentos_dic_2025/main/models/data/predicciones_aciertos_btcusd.parquet",
    'EURUSD': "https://raw.githubusercontent.com/aliskairraul/Inferencias_instrumentos_dic_2025/main/models/data/predicciones_aciertos_eurusd.parquet",
    'SPX': "https://raw.githubusercontent.com/aliskairraul/Inferencias_instrumentos_dic_2025/main/models/data/predicciones_aciertos_spx.parquet",
    'XAUUSD': "https://raw.githubusercontent.com/aliskairraul/Inferencias_instrumentos_dic_2025/main/models/data/predicciones_aciertos_xauusd.parquet",
}

paths_data_github = {
    "BTCUSD": Path("data/proviene_github/predicciones_aciertos_btcusd.parquet"),
    "EURUSD": Path("data/proviene_github/predicciones_aciertos_eurusd.parquet"),
    "SPX": Path("data/proviene_github/predicciones_aciertos_spx.parquet"),
    "XAUUSD": Path("data/proviene_github/predicciones_aciertos_xauusd.parquet")
}

paths_data_por_libreria = {
    "sklearn" : Path("data/data_por_librerias/predicciones_aciertos_sklearn.parquet"),
    "lightgbm" : Path("data/data_por_librerias/predicciones_aciertos_lightgbm.parquet"),
    "xgboost" : Path("data/data_por_librerias/predicciones_aciertos_xgboost.parquet"),
    "pytorch" : Path("data/data_por_librerias/predicciones_aciertos_pytorch.parquet"),
    "tensorflow" : Path("data/data_por_librerias/predicciones_aciertos_tensorflow.parquet"),
}

paths_backtesting_por_instrumento = {
    "BTCUSD": Path("data/backtesting/backtesting_btcusd.parquet"),
    "EURUSD": Path("data/backtesting/backtesting_eurusd.parquet"),
    "SPX": Path("data/backtesting/backtesting_spx.parquet"),
    "XAUUSD": Path("data/backtesting/backtesting_xauusd.parquet")
}

paths_backtesting_por_libreria = {
    "sklearn" : Path("data/backtesting/bactesting_sklearn.parquet"),
    "lightgbm" : Path("data/backtesting/bactesting_lightgbm.parquet"),
    "xgboost" : Path("data/backtesting/bactesting_xgboost.parquet"),
    "pytorch" : Path("data/backtesting/bactesting_pytorch.parquet"),
    "tensorflow" : Path("data/backtesting/bactesting_tensorflow.parquet"),
}

paths_backtesting_instrumento_por_libreria = {
    "back_btc_sklearn": Path("data/backtesting/backtesting_btc_sklearn.parquet"),
    "back_btc_lightgbm": Path("data/backtesting/backtesting_btc_lightgbm.parquet"),
    "back_btc_xgboost": Path("data/backtesting/backtesting_btc_xgboost.parquet"),
    "back_btc_pytorch": Path("data/backtesting/backtesting_btc_pytorch.parquet"),
    "back_btc_tensorflow": Path("data/backtesting/backtesting_btc_tensorflow.parquet"),

    "back_eur_sklearn": Path("data/backtesting/backtesting_eur_sklearn.parquet"),
    "back_eur_lightgbm": Path("data/backtesting/backtesting_eur_lightgbm.parquet"),
    "back_eur_xgboost": Path("data/backtesting/backtesting_eur_xgboost.parquet"),
    "back_eur_pytorch": Path("data/backtesting/backtesting_eur_pytorch.parquet"),
    "back_eur_tensorflow": Path("data/backtesting/backtesting_eur_tensorflow.parquet"),

    "back_xau_sklearn": Path("data/backtesting/backtesting_xau_sklearn.parquet"),
    "back_xau_lightgbm": Path("data/backtesting/backtesting_xau_lightgbm.parquet"),
    "back_xau_xgboost": Path("data/backtesting/backtesting_xau_xgboost.parquet"),
    "back_xau_pytorch": Path("data/backtesting/backtesting_xau_pytorch.parquet"),
    "back_xau_tensorflow": Path("data/backtesting/backtesting_xau_tensorflow.parquet"),

    "back_spx_sklearn": Path("data/backtesting/backtesting_spx_sklearn.parquet"),
    "back_spx_lightgbm": Path("data/backtesting/backtesting_spx_lightgbm.parquet"),
    "back_spx_xgboost": Path("data/backtesting/backtesting_spx_xgboost.parquet"),
    "back_spx_pytorch": Path("data/backtesting/backtesting_spx_pytorch.parquet"),
    "back_spx_tensorflow": Path("data/backtesting/backtesting_spx_tensorflow.parquet"),
}

path_portafolio = Path("data/backtesting/bactesting_portafolio.parquet")

diccionario_drop = {
    "S&P 500 solo Sklearn" : "df_back_spx_sklearn",
    "S&P 500 solo LightGbm" : "df_back_spx_lightgbm",
    "S&P 500 solo XgBoost" : "df_back_spx_xgboost",
    "S&P 500 solo PyTorch" : "df_back_spx_pytorch",
    "S&P 500 solo TensorFlow" : "df_back_spx_tensorflow",
    "EURUSD solo Sklearn" : "df_back_eur_sklearn",
    "EURUSD solo LightGbm" : "df_back_eur_lightgbm",
    "EURUSD solo XgBoost" : "df_back_eur_xgboost",
    "EURUSD solo PyTorch" : "df_back_eur_pytorch",
    "EURUSD solo TensorFlow" : "df_back_eur_tensorflow",
    "BTCUSD solo Sklearn" : "df_back_btc_sklearn",
    "BTCUSD solo LightGbm" : "df_back_btc_lightgbm",
    "BTCUSD solo XgBoost" : "df_back_btc_xgboost",
    "BTCUSD solo TensorFlow" : "df_back_btc_tensorflow",
    "XAUUSD solo Sklearn" : "df_back_xau_sklearn",
    "XAUUSD solo LightGbm" : "df_back_xau_lightgbm",
    "XAUUSD solo XgBoost" : "df_back_xau_xgboost",
    "XAUUSD solo TensorFlow" : "df_back_xau_tensorflow",
}

colores_hex = {
    "eurusd": "#6ED180",  
    "btcusd": "#ff8c00", 
    "xauusd": "#fffa5c", 
    "spx": "#54A6DC", 
    "sklearn": "#2e8b57", 
    "lightgbm": "#ff8c00", 
    "xgboost": "#4169e1", 
    "pytorch": "#3A0603", 
    "tensorflow": "#ab63fa", 
    "up": "#79CA7C",
    "down": "#FF0000",
}

keys_datos = [
    "btcusd",
    "eurusd",
    "xauusd",
    "spx",
    "sklearn",
    "lightgbm",
    "xgboost",
    "pytorch",
    "tensorflow",
    "back_btc",
    "back_eur",
    "back_xau",
    "back_spx",
    "df_back_sklearn",
    "df_back_lightgbm",
    "df_back_xgboost",
    "df_back_pytorch",
    "df_back_tensorflow",
    "df_back_btc_sklearn",
    "df_back_btc_lightgbm",
    "df_back_btc_xgboost",
    "df_back_btc_tensorflow",
    "df_back_eur_sklearn",
    "df_back_eur_lightgbm",
    "df_back_eur_xgboost",
    "df_back_eur_pytorch",
    "df_back_eur_tensorflow",
    "df_back_xau_sklearn",
    "df_back_xau_lightgbm",
    "df_back_xau_xgboost",
    "df_back_xau_tensorflow",
    "df_back_spx_sklearn",
    "df_back_spx_lightgbm",
    "df_back_spx_xgboost",
    "df_back_spx_pytorch",
    "df_back_spx_tensorflow",
    "portafolio",
    "evolution_capital",
    "summary_winrate"
 ]