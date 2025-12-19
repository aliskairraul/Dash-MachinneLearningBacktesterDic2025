import polars as pl
from utils.utils import paths_data_github


def backtesting_btcusd_x_libreria(df: pl.DataFrame, libreria: str, transaction_cost_pct: float = 0.002,
                                  monto_inicial: float = 10000.0) -> pl.DataFrame:
    modelo = libreria + "_01"
    if modelo not in df.columns:
        return pl.DataFrame()

    estrategia = modelo.replace("01", "estrategia")
    opero = modelo.replace("01", "opero")
    acierto = modelo.replace("01", "acierto")

    columnas = ["date", "close", "close_tomorrow", "target_direction", modelo, estrategia, opero, acierto]
    columnas_nuevas = ["date", "close", "close_tomorrow", "target_direction", "modelo", "estrategia", "operaciones", "aciertos"]

    df = df.select(columnas)
    df.columns = columnas_nuevas

    prices = df["close"].to_list()
    prices_tomorrow = df["close_tomorrow"].to_list()
    operaciones = df["operaciones"].to_list()
    aciertos = df["aciertos"].to_list()
    montos_inicios_dia = []
    montos_fin_dia = []
    monto_disponible = 0
    monto_final_dia = 0

    for i in range(len(prices)):
        if i == 0:
            montos_inicios_dia.append(monto_inicial)
            monto_disponible = monto_inicial
        else:
            montos_inicios_dia.append(montos_fin_dia[i - 1])
            monto_disponible = montos_fin_dia[i - 1]

        operacion = operaciones[i]
        acierto = aciertos[i]

        if operacion == 0:
            montos_fin_dia.append(monto_disponible)
            continue

        cambio_porcentual = abs((prices_tomorrow[i] - prices[i]) / prices[i])
        costo_operacion = monto_disponible * transaction_cost_pct

        if acierto == 1:
            ganancia = monto_disponible * cambio_porcentual
            monto_final_dia = monto_disponible + ganancia - costo_operacion
            montos_fin_dia.append(monto_final_dia)
            continue
        else:
            perdida = monto_disponible * cambio_porcentual
            monto_final_dia = monto_disponible - perdida - costo_operacion
            montos_fin_dia.append(monto_final_dia)

    df = df.with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ])
    return df


def backtesting_eurusd_x_libreria(df: pl.DataFrame, libreria: str, transaction_cost_pips: float = 1.5, monto_inicial: float = 10000.0,
                                  lotaje: float = 1.0) -> pl.DataFrame:
    modelo = libreria + "_01"
    if modelo not in df.columns:
        return pl.DataFrame()

    estrategia = modelo.replace("01", "estrategia")
    opero = modelo.replace("01", "opero")
    acierto = modelo.replace("01", "acierto")

    columnas = ["date", "close", "close_tomorrow", "target_direction", modelo, estrategia, opero, acierto]
    columnas_nuevas = ["date", "close", "close_tomorrow", "target_direction", "modelo", "estrategia", "operaciones", "aciertos"]

    df = df.select(columnas)
    df.columns = columnas_nuevas

    prices = df["close"].to_list()
    prices_tomorrow = df["close_tomorrow"].to_list()
    operaciones = df["operaciones"].to_list()
    aciertos = df["aciertos"].to_list()
    montos_inicios_dia = []
    montos_fin_dia = []
    monto_disponible = 0
    monto_final_dia = 0

    for i in range(len(prices)):
        if i == 0:
            montos_inicios_dia.append(monto_inicial)
            monto_disponible = monto_inicial
        else:
            montos_inicios_dia.append(montos_fin_dia[i - 1])
            monto_disponible = montos_fin_dia[i - 1]

        operacion = operaciones[i]
        acierto = aciertos[i]

        if operacion == 0:
            montos_fin_dia.append(monto_disponible)
            continue

        variacion_pips = round(abs(prices_tomorrow[i] - prices[i]), 4) * 10000
        valor_pip = 10 * lotaje

        if acierto == 1:
            ganancia = valor_pip * (variacion_pips - transaction_cost_pips)
            monto_final_dia = monto_disponible + ganancia
            montos_fin_dia.append(monto_final_dia)
            continue
        else:
            perdida = valor_pip * (variacion_pips + transaction_cost_pips)
            monto_final_dia = monto_disponible - perdida
            montos_fin_dia.append(monto_final_dia)
            continue

    df = df.with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ])
    return df


def backtesting_xauusd_x_libreria(df: pl.DataFrame, libreria: str, transaction_cost_onza_controlada: float = 0.37,
                                  monto_inicial: float = 10000.0, lotaje: float = 0.1) -> pl.DataFrame:
    modelo = libreria + "_01"
    if modelo not in df.columns:
        return pl.DataFrame()

    estrategia = modelo.replace("01", "estrategia")
    opero = modelo.replace("01", "opero")
    acierto = modelo.replace("01", "acierto")

    columnas = ["date", "close", "close_tomorrow", "target_direction", modelo, estrategia, opero, acierto]
    columnas_nuevas = ["date", "close", "close_tomorrow", "target_direction", "modelo", "estrategia", "operaciones", "aciertos"]

    df = df.select(columnas)
    df.columns = columnas_nuevas

    prices = df["close"].to_list()
    prices_tomorrow = df["close_tomorrow"].to_list()
    operaciones = df["operaciones"].to_list()
    aciertos = df["aciertos"].to_list()
    montos_inicios_dia = []
    montos_fin_dia = []
    monto_disponible = 0
    monto_final_dia = 0

    for i in range(len(prices)):
        if i == 0:
            montos_inicios_dia.append(monto_inicial)
            monto_disponible = monto_inicial
        else:
            montos_inicios_dia.append(montos_fin_dia[i - 1])
            monto_disponible = montos_fin_dia[i - 1]

        operacion = operaciones[i]
        acierto = aciertos[i]

        if operacion == 0:
            montos_fin_dia.append(monto_disponible)
            continue

        variacion_precio = abs(prices_tomorrow[i] - prices[i])
        onzas_controladas = lotaje * 100
        costo_operacion = transaction_cost_onza_controlada * onzas_controladas

        if acierto == 1:
            ganancia = variacion_precio * onzas_controladas
            monto_final_dia = monto_disponible + ganancia - costo_operacion
            montos_fin_dia.append(monto_final_dia)
        else:
            perdida = variacion_precio * onzas_controladas
            monto_final_dia = monto_disponible - perdida - costo_operacion
            montos_fin_dia.append(monto_final_dia)

    df = df.with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ])

    return df


def backtesting_spx_x_libreria(df: pl.DataFrame, libreria: str, transaction_total_point_cost: float = 12.0,
                               monto_inicial: float = 10000.0, lotaje: float = 1.0) -> pl.DataFrame:
    DOLARES_LOTAJE_X_PUNTO_BROKER_CFD = 10

    modelo = libreria + "_01"
    if modelo not in df.columns:
        return pl.DataFrame()

    estrategia = modelo.replace("01", "estrategia")
    opero = modelo.replace("01", "opero")
    acierto = modelo.replace("01", "acierto")

    columnas = ["date", "close", "close_tomorrow", "target_direction", modelo, estrategia, opero, acierto]
    columnas_nuevas = ["date", "close", "close_tomorrow", "target_direction", "modelo", "estrategia", "operaciones", "aciertos"]

    df = df.select(columnas)
    df.columns = columnas_nuevas

    puntos_iniciales_list = df["close"].to_list()
    puntos_finales_list = df["close_tomorrow"].to_list()
    operaciones = df["operaciones"].to_list()
    aciertos = df["aciertos"].to_list()
    montos_inicios_dia = []
    montos_fin_dia = []
    monto_disponible = 0
    monto_final_dia = 0

    for i in range(len(puntos_iniciales_list)):
        if i == 0:
            montos_inicios_dia.append(monto_inicial)
            monto_disponible = monto_inicial
        else:
            montos_inicios_dia.append(montos_fin_dia[i - 1])
            monto_disponible = montos_fin_dia[i - 1]

        operacion = operaciones[i]
        acierto = aciertos[i]

        if operacion == 0:
            montos_fin_dia.append(monto_disponible)
            continue

        variacion_puntos = abs(puntos_finales_list[i] - puntos_iniciales_list[i])
        costo_operacion = transaction_total_point_cost * lotaje

        if acierto == 1:
            ganancia = variacion_puntos * DOLARES_LOTAJE_X_PUNTO_BROKER_CFD * lotaje
            monto_final_dia = monto_disponible + ganancia - costo_operacion
            montos_fin_dia.append(monto_final_dia)
            continue
        else:
            perdida = variacion_puntos * DOLARES_LOTAJE_X_PUNTO_BROKER_CFD * lotaje
            monto_final_dia = monto_disponible - perdida - costo_operacion
            montos_fin_dia.append(monto_final_dia)

    df = df.with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ])
    return df
