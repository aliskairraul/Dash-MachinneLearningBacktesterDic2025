import polars as pl
from datetime import datetime
from utils.utils import paths_data_github, paths_data_por_libreria


def instrumento_to_libreria(df: pl.dataframe, libreria: str, instrumento: str, dia: datetime.date) -> dict:
    dias_df = df["date"].to_list()
    columna_close = instrumento + "_close"
    columna_tomorrow = instrumento + "_tomorrow"
    columna_target_d = instrumento + "_targetd"
    columna_prediccion = instrumento + "_predict"
    columna_estrategia = instrumento + "_estrategia"
    columna_opero = instrumento + "_opero"
    columna_acierto = instrumento + "_acierto"

    if dia not in dias_df:
        return {
            columna_close: 0.0,
            columna_tomorrow: 0.0,
            columna_target_d: 0,
            columna_prediccion: 0,
            columna_estrategia: "",
            columna_opero: 0,
            columna_acierto: 0
        }

    mask = df["date"] == dia
    modelo = libreria + "_01"
    estrategia = libreria + "_estrategia"
    opero = libreria + "_opero"
    acierto = libreria + "_acierto"

    return {
        columna_close: df.filter(mask)["close"][0],
        columna_tomorrow: df.filter(mask)["close_tomorrow"][0],
        columna_target_d: df.filter(mask)["target_direction"][0],
        columna_prediccion: df.filter(mask)[modelo][0],
        columna_estrategia: df.filter(mask)[estrategia][0],
        columna_opero: df.filter(mask)[opero][0],
        columna_acierto: df.filter(mask)[acierto][0],
    }


def pasar_data_de_instrumentos_a_librerias() -> None:
    df_btcusd = pl.read_parquet(paths_data_github["BTCUSD"]).sort("date")
    df_eurusd = pl.read_parquet(paths_data_github["EURUSD"]).sort("date")
    df_xauusd = pl.read_parquet(paths_data_github["XAUUSD"]).sort("date")
    df_spx = pl.read_parquet(paths_data_github["SPX"]).sort("date")

    dates = df_btcusd["date"].to_list()
    librerias = ["sklearn", "lightgbm", "xgboost", "pytorch", "tensorflow"]

    for libreria in librerias:
        data = []
        for dia in dates:
            diccionario = {"date": dia}
            modelo = libreria + "_01"
            if modelo in df_btcusd.columns:
                diccionario_btcusd = instrumento_to_libreria(df=df_btcusd, libreria=libreria, instrumento="btcusd", dia=dia)
                diccionario = diccionario | diccionario_btcusd
            if modelo in df_eurusd.columns:
                diccionario_eurusd = instrumento_to_libreria(df=df_eurusd, libreria=libreria, instrumento="eurusd", dia=dia)
                diccionario = diccionario | diccionario_eurusd
            if modelo in df_xauusd.columns:
                diccionario_xauusd = instrumento_to_libreria(df=df_xauusd, libreria=libreria, instrumento="xauusd", dia=dia)
                diccionario = diccionario | diccionario_xauusd
            if modelo in df_spx.columns:
                diccionario_spx = instrumento_to_libreria(df=df_spx, libreria=libreria, instrumento="spx", dia=dia)
                diccionario = diccionario | diccionario_spx

            data.append(diccionario)

        df = pl.DataFrame(data)
        df.write_parquet(paths_data_por_libreria[libreria])
