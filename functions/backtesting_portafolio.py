import polars as pl
import numpy as np


def cargar_datos(df_sklearn: pl.DataFrame, df_lightgbm: pl.DataFrame, df_xgboost: pl.DataFrame,
                 df_pytorch: pl.DataFrame, df_tensorflow: pl.DataFrame) -> tuple[dict, np.array, np.array]:

    dfs = [df_sklearn, df_lightgbm, df_xgboost, df_pytorch, df_tensorflow]

    columnas_opero = ['btcusd_opero', 'eurusd_opero', 'xauusd_opero', 'spx_opero']
    columnas_acierto = ['btcusd_acierto', 'eurusd_acierto', 'xauusd_acierto', 'spx_acierto']
    columnas_close = ['btcusd_close', 'eurusd_close', 'xauusd_close', 'spx_close']
    columnas_tomorrow = ['btcusd_tomorrow', 'eurusd_tomorrow', 'xauusd_tomorrow', 'spx_tomorrow']

    arreglo_opero_btc = np.zeros(df_tensorflow.shape[0])
    arreglo_acierto_btc = np.zeros(df_tensorflow.shape[0])

    arreglo_opero_eur = np.zeros(df_tensorflow.shape[0])
    arreglo_acierto_eur = np.zeros(df_tensorflow.shape[0])

    arreglo_opero_xau = np.zeros(df_tensorflow.shape[0])
    arreglo_acierto_xau = np.zeros(df_tensorflow.shape[0])

    arreglo_opero_spx = np.zeros(df_tensorflow.shape[0])
    arreglo_acierto_spx = np.zeros(df_tensorflow.shape[0])

    arreglos_opero = [arreglo_opero_btc, arreglo_opero_eur, arreglo_opero_xau, arreglo_opero_spx]
    arreglos_acierto = [arreglo_acierto_btc, arreglo_acierto_eur, arreglo_acierto_xau, arreglo_acierto_spx]

    arreglos_close = []
    arreglos_tomorrow = []

    encontro_closes = [False, False, False, False]

    for i in range(4):
        for j in range(5):
            if columnas_opero[i] in dfs[j].columns:
                arreglos_opero[i] += dfs[j].sort("date")[columnas_opero[i]].to_numpy()
                arreglos_acierto[i] += dfs[j].sort("date")[columnas_acierto[i]].to_numpy()

                if not encontro_closes[i]:
                    arreglos_close.append(dfs[j].sort("date")[columnas_close[i]].to_numpy())
                    arreglos_tomorrow.append(dfs[j].sort("date")[columnas_tomorrow[i]].to_numpy())
                    encontro_closes[i] = True

    datos = {
        "BTCUSD": {},
        "EURUSD": {},
        "SPX": {},
        "XAUUSD": {}
    }

    datos["BTCUSD"]["close"] = arreglos_close[0]
    datos["BTCUSD"]["tomorrow"] = arreglos_tomorrow[0]
    datos["BTCUSD"]["opero"] = arreglo_opero_btc
    datos["BTCUSD"]["acierto"] = arreglo_acierto_btc

    datos["EURUSD"]["close"] = arreglos_close[1]
    datos["EURUSD"]["tomorrow"] = arreglos_tomorrow[1]
    datos["EURUSD"]["opero"] = arreglo_opero_eur
    datos["EURUSD"]["acierto"] = arreglo_acierto_eur

    datos["XAUUSD"]["close"] = arreglos_close[2]
    datos["XAUUSD"]["tomorrow"] = arreglos_tomorrow[2]
    datos["XAUUSD"]["opero"] = arreglo_opero_xau
    datos["XAUUSD"]["acierto"] = arreglo_acierto_xau

    datos["SPX"]["close"] = arreglos_close[3]
    datos["SPX"]["tomorrow"] = arreglos_tomorrow[3]
    datos["SPX"]["opero"] = arreglo_opero_spx
    datos["SPX"]["acierto"] = arreglo_acierto_spx

    operaciones = arreglo_opero_btc + arreglo_opero_eur + arreglo_opero_xau + arreglo_opero_spx
    aciertos = arreglo_acierto_btc + arreglo_acierto_eur + arreglo_acierto_xau + arreglo_acierto_spx

    return (datos, operaciones, aciertos)


def operacion_diaria_btcusd(monto_por_operacion: float,
                            close: float,
                            tomorrow: float,
                            operaciones_solo_instrumento: int,
                            aciertos: int,
                            transaction_cost_pct: float = 0.002,) -> float:
    monto_retornar = monto_por_operacion * operaciones_solo_instrumento
    no_aciertos = operaciones_solo_instrumento - aciertos
    if aciertos == no_aciertos:
        return monto_retornar
    cambio_porcentual = abs((tomorrow - close) / close)
    costo_por_operacion = monto_por_operacion * transaction_cost_pct
    if aciertos > no_aciertos:
        ganancia = (aciertos - no_aciertos) * monto_por_operacion * cambio_porcentual
        costo_operacional = costo_por_operacion * (aciertos - no_aciertos)
        monto_retornar = monto_retornar + ganancia - costo_operacional
    else:
        perdida = (no_aciertos - aciertos) * monto_por_operacion * cambio_porcentual
        costo_operacional = costo_por_operacion * (no_aciertos - aciertos)
        monto_retornar = monto_retornar - perdida - costo_operacional
    return monto_retornar


def operacion_diaria_eurusd(monto_por_operacion: float,
                            close: float,
                            tomorrow: float,
                            operaciones_solo_instrumento: int,
                            aciertos: int,
                            total_operaciones: int,
                            transaction_cost_pips: float = 1.5,
                            lotaje: float = 1.0) -> float:
    monto_retornar = monto_por_operacion * operaciones_solo_instrumento
    no_aciertos = operaciones_solo_instrumento - aciertos
    if aciertos == no_aciertos:
        return monto_retornar
    variacion_pips = round(abs(tomorrow - close), 4) * 10000
    lotaje_de_acuerdo_a_operaciones = round(((lotaje * operaciones_solo_instrumento) / total_operaciones), 2)
    valor_pip = 10 * lotaje_de_acuerdo_a_operaciones
    if aciertos > no_aciertos:
        ganancia = (aciertos - no_aciertos) * valor_pip * (variacion_pips - transaction_cost_pips)
        monto_retornar += ganancia
    else:
        perdida = (no_aciertos - aciertos) * valor_pip * (variacion_pips + transaction_cost_pips)
        monto_retornar -= perdida
    return monto_retornar


def operacion_diaria_xauusd(monto_por_operacion: float,
                            close: float,
                            tomorrow: float,
                            operaciones_solo_instrumento: int,
                            aciertos: int,
                            total_operaciones: int,
                            transaction_cost_onza_controlada: float = 0.37,
                            lotaje: float = 0.1) -> float:
    monto_retornar = monto_por_operacion * operaciones_solo_instrumento
    no_aciertos = operaciones_solo_instrumento - aciertos
    if aciertos == no_aciertos:
        return monto_retornar

    variacion_precio = abs(tomorrow - close)
    lotaje_de_acuerdo_a_operaciones = round(((lotaje * operaciones_solo_instrumento) / total_operaciones), 2)
    onzas_controladas = lotaje_de_acuerdo_a_operaciones * 100
    costo_por_operacion = transaction_cost_onza_controlada * onzas_controladas

    if aciertos > no_aciertos:
        ganancia = variacion_precio * onzas_controladas * (aciertos - no_aciertos)
        costo_operacional = costo_por_operacion * (aciertos - no_aciertos)
        monto_retornar = monto_retornar + ganancia - costo_operacional
    else:
        perdida = variacion_precio * onzas_controladas * (no_aciertos - aciertos)
        costo_operacional = costo_por_operacion * (no_aciertos - aciertos)
        monto_retornar = monto_retornar - perdida - costo_operacional
    return monto_retornar


def operacion_diaria_spx(monto_por_operacion: float,
                         close: float,
                         tomorrow: float,
                         operaciones_solo_instrumento: int,
                         aciertos: int,
                         total_operaciones: int,
                         transaction_total_point_cost: float = 0.8,
                         lotaje: float = 1.0) -> float:
    DOLARES_LOTAJE_X_PUNTO_BROKER_CFD = 10
    monto_retornar = monto_por_operacion * operaciones_solo_instrumento
    no_aciertos = operaciones_solo_instrumento - aciertos
    if aciertos == no_aciertos:
        return monto_retornar
    variacion_puntos = abs(tomorrow - close)
    lotaje_de_acuerdo_a_operaciones = round((lotaje / total_operaciones), 2)
    costo_por_operacion = transaction_total_point_cost * lotaje_de_acuerdo_a_operaciones

    if aciertos > no_aciertos:
        ganancia = variacion_puntos * DOLARES_LOTAJE_X_PUNTO_BROKER_CFD * lotaje_de_acuerdo_a_operaciones * (aciertos - no_aciertos)
        costo_operacional = costo_por_operacion * (aciertos - no_aciertos)
        monto_retornar = monto_retornar + ganancia - costo_operacional
    else:
        perdida = variacion_puntos * DOLARES_LOTAJE_X_PUNTO_BROKER_CFD * lotaje_de_acuerdo_a_operaciones * (no_aciertos - aciertos)
        costo_operacional = costo_por_operacion * (no_aciertos - aciertos)
        monto_retornar = monto_retornar - perdida - costo_operacional
    return monto_retornar


def backtesting_portafolio(df_sklearn: pl.DataFrame, df_lightgbm: pl.DataFrame, df_xgboost: pl.DataFrame,
                           df_pytorch: pl.DataFrame, df_tensorflow: pl.DataFrame, monto_inicial: float = 10000.0):
    datos, operaciones_dia, aciertos_dia = cargar_datos(df_sklearn=df_sklearn, df_lightgbm=df_lightgbm, df_xgboost=df_xgboost,
                                                        df_pytorch=df_pytorch, df_tensorflow=df_tensorflow)

    df_retornar = pl.DataFrame().with_columns(pl.Series(df_sklearn["date"]))
    montos_inicios_dia = []
    montos_fin_dia = []
    monto_disponible = 0

    for i in range(len(operaciones_dia)):
        if i == 0:
            montos_inicios_dia.append(monto_inicial)
            monto_disponible = monto_inicial
        else:
            montos_inicios_dia.append(montos_fin_dia[i - 1])
            monto_disponible = montos_fin_dia[i - 1]

        operaciones = operaciones_dia[i]

        if operaciones == 0:
            montos_fin_dia.append(monto_disponible)
            continue

        acumulado_montos = []
        monto_disponible_por_operacion = round((monto_disponible / operaciones), 2)

        if datos["BTCUSD"]["opero"][i] > 0:
            operaciones_instrumento = datos["BTCUSD"]["opero"][i]
            close = datos["BTCUSD"]["close"][i]
            tomorrow = datos["BTCUSD"]["tomorrow"][i]
            acierto = datos["BTCUSD"]["acierto"][i]
            monto = operacion_diaria_btcusd(monto_por_operacion=monto_disponible_por_operacion,
                                            close=close,
                                            tomorrow=tomorrow,
                                            operaciones_solo_instrumento=operaciones_instrumento,
                                            aciertos=acierto)
            acumulado_montos.append(monto)

        if datos["EURUSD"]["opero"][i] > 0:
            operaciones_instrumento = datos["EURUSD"]["opero"][i]
            close = datos["EURUSD"]["close"][i]
            tomorrow = datos["EURUSD"]["tomorrow"][i]
            acierto = datos["EURUSD"]["acierto"][i]
            monto = operacion_diaria_eurusd(monto_por_operacion=monto_disponible_por_operacion,
                                            close=close,
                                            tomorrow=tomorrow,
                                            operaciones_solo_instrumento=operaciones_instrumento,
                                            aciertos=acierto,
                                            total_operaciones=operaciones)
            acumulado_montos.append(monto)

        if datos["XAUUSD"]["opero"][i] > 0:
            operaciones_instrumento = datos["XAUUSD"]["opero"][i]
            close = datos["XAUUSD"]["close"][i]
            tomorrow = datos["XAUUSD"]["tomorrow"][i]
            acierto = datos["XAUUSD"]["acierto"][i]
            monto = operacion_diaria_xauusd(monto_por_operacion=monto_disponible_por_operacion,
                                            close=close,
                                            tomorrow=tomorrow,
                                            operaciones_solo_instrumento=operaciones_instrumento,
                                            aciertos=acierto,
                                            total_operaciones=operaciones)
            acumulado_montos.append(monto)

        if datos["SPX"]["opero"][i] > 0:
            operaciones_instrumento = datos["SPX"]["opero"][i]
            close = datos["SPX"]["close"][i]
            tomorrow = datos["SPX"]["tomorrow"][i]
            acierto = datos["SPX"]["acierto"][i]
            monto = operacion_diaria_spx(monto_por_operacion=monto_disponible_por_operacion,
                                         close=close,
                                         tomorrow=tomorrow,
                                         operaciones_solo_instrumento=operaciones_instrumento,
                                         aciertos=acierto,
                                         total_operaciones=operaciones)
            acumulado_montos.append(monto)

        monto_final_dia = 0
        for i in range(len(acumulado_montos)):
            monto_final_dia += acumulado_montos[i]

        montos_fin_dia.append(monto_final_dia)

    df_retornar = df_retornar.with_columns([
        pl.Series(name="Operaciones", values=operaciones_dia).cast(pl.Int16),
        pl.Series(name="Aciertos", values=aciertos_dia).cast(pl.Int16),
        pl.Series(name="Fallos", values=(operaciones_dia - aciertos_dia)).cast(pl.Int16),
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ])
    return df_retornar
