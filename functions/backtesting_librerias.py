import polars as pl


def carga_datos(df: pl.DataFrame) -> tuple[dict, dict, list, list]:
    """_summary_
    Nota: El diccionario datos se pudo haber realizado con un ciclo for con menos codigo.  Lo dejo de esta manera para que sea mas facil de
          entender para cuando revise esto en el futuro. La lógica de como se acomodaron los datos en diccionarios anidados, no suelo programarla,
          pero en este caso considere era lo practico de hacer

    Args:
        df (pl.DataFrame): _description_

    Returns:
        tuple[dict, dict, list, list]: _description_
    """
    columnas_operaciones = []
    columnas_aciertos = []
    datos = {
        "BTCUSD": {},
        "EURUSD": {},
        "SPX": {},
        "XAUUSD": {}
    }
    existe = {
        "BTCUSD": False,
        "EURUSD": False,
        "SPX": False,
        "XAUUSD": False
    }

    if "btcusd_close" in df.columns:
        columnas_operaciones.append("btcusd_opero")
        columnas_aciertos.append("btcusd_acierto")
        existe["BTCUSD"] = True
        datos["BTCUSD"]["close"] = df.sort("date")["btcusd_close"].to_list()
        datos["BTCUSD"]["tomorrow"] = df.sort("date")["btcusd_tomorrow"].to_list()
        datos["BTCUSD"]["opero"] = df.sort("date")["btcusd_opero"].to_list()
        datos["BTCUSD"]["acierto"] = df.sort("date")["btcusd_acierto"].to_list()

    if "eurusd_close" in df.columns:
        columnas_operaciones.append("eurusd_opero")
        columnas_aciertos.append("eurusd_acierto")
        existe["EURUSD"] = True
        datos["EURUSD"]["close"] = df.sort("date")["eurusd_close"].to_list()
        datos["EURUSD"]["tomorrow"] = df.sort("date")["eurusd_tomorrow"].to_list()
        datos["EURUSD"]["opero"] = df.sort("date")["eurusd_opero"].to_list()
        datos["EURUSD"]["acierto"] = df.sort("date")["eurusd_acierto"].to_list()

    if "xauusd_close" in df.columns:
        columnas_operaciones.append("xauusd_opero")
        columnas_aciertos.append("xauusd_acierto")
        existe["XAUUSD"] = True
        datos["XAUUSD"]["close"] = df.sort("date")["xauusd_close"].to_list()
        datos["XAUUSD"]["tomorrow"] = df.sort("date")["xauusd_tomorrow"].to_list()
        datos["XAUUSD"]["opero"] = df.sort("date")["xauusd_opero"].to_list()
        datos["XAUUSD"]["acierto"] = df.sort("date")["xauusd_acierto"].to_list()

    if "spx_close" in df.columns:
        columnas_operaciones.append("spx_opero")
        columnas_aciertos.append("spx_acierto")
        existe["SPX"] = True
        datos["SPX"]["close"] = df.sort("date")["spx_close"].to_list()
        datos["SPX"]["tomorrow"] = df.sort("date")["spx_tomorrow"].to_list()
        datos["SPX"]["opero"] = df.sort("date")["spx_opero"].to_list()
        datos["SPX"]["acierto"] = df.sort("date")["spx_acierto"].to_list()

        return (datos, existe, columnas_aciertos, columnas_operaciones)


def operacion_diaria_btcusd(monto: float, close: float, tomorrow: float, acierto: int, transaction_cost_pct: float = 0.002) -> float:
    monto_retornar = 0
    cambio_porcentual = abs((tomorrow - close) / close)
    costo_operacion = monto * transaction_cost_pct
    if acierto == 1:
        ganancia = monto * cambio_porcentual
        monto_retornar = monto + ganancia - costo_operacion
    else:
        perdida = monto * cambio_porcentual
        monto_retornar = monto - perdida - costo_operacion
    return monto_retornar


def operacion_diaria_eurusd(monto: float, close: float, tomorrow: float, acierto: int, total_operaciones: int,
                            transaction_cost_pips: float = 1.5, lotaje: float = 1) -> float:
    monto_retornar = 0
    variacion_pips = round(abs(tomorrow - close), 4) * 10000
    lotaje_de_acuerdo_a_operaciones = round((lotaje / total_operaciones), 2)
    valor_pip = 10 * lotaje_de_acuerdo_a_operaciones
    if acierto == 1:
        ganancia = valor_pip * (variacion_pips - transaction_cost_pips)
        monto_retornar = monto + ganancia
    else:
        perdida = valor_pip * (variacion_pips + transaction_cost_pips)
        monto_retornar = monto - perdida
    return monto_retornar


def operacion_diaria_xauusd(monto: float, close: float, tomorrow: float, acierto: int, total_operaciones: int,
                            transaction_cost_onza_controlada: float = 0.37, lotaje: float = 0.1) -> float:
    monto_retornar = 0
    variacion_precio = abs(tomorrow - close)
    lotaje_de_acuerdo_a_operaciones = round((lotaje / total_operaciones), 2)
    onzas_controladas = lotaje_de_acuerdo_a_operaciones * 100
    costo_operacion = transaction_cost_onza_controlada * onzas_controladas

    if acierto == 1:
        ganancia = variacion_precio * onzas_controladas
        monto_retornar = monto + ganancia - costo_operacion
    else:
        perdida = variacion_precio * onzas_controladas
        monto_retornar = monto - perdida - costo_operacion
    return monto_retornar


def operacion_diaria_spx(monto: float, close: float, tomorrow: float, acierto: int, total_operaciones: int,
                         transaction_total_point_cost: float = 12.0, lotaje: float = 1.0) -> float:
    monto_retornar = 0
    DOLARES_LOTAJE_X_PUNTO_BROKER_CFD = 10
    variacion_puntos = abs(tomorrow - close)
    lotaje_de_acuerdo_a_operaciones = round((lotaje / total_operaciones), 2)
    costo_por_operacion = transaction_total_point_cost * lotaje_de_acuerdo_a_operaciones

    if acierto == 1:
        ganancia = variacion_puntos * DOLARES_LOTAJE_X_PUNTO_BROKER_CFD * lotaje_de_acuerdo_a_operaciones
        monto_retornar = monto + ganancia - costo_por_operacion
    else:
        perdida = variacion_puntos * DOLARES_LOTAJE_X_PUNTO_BROKER_CFD * lotaje_de_acuerdo_a_operaciones
        monto_retornar = monto - perdida - costo_por_operacion
    return monto_retornar


def backtesting_librerias(df: pl.dataframe, monto_inicial: float = 10000.0) -> pl.DataFrame:
    datos, existe, columnas_aciertos, columnas_operaciones = carga_datos(df=df)
    df = df.with_columns([
        pl.sum_horizontal(pl.col(columnas_operaciones)).alias("operaciones_dia"),
        pl.sum_horizontal(pl.col(columnas_aciertos)).alias("aciertos_dia")
    ]).sort("date")

    operaciones_dia = df["operaciones_dia"].to_list()
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

        if existe["BTCUSD"]:
            if datos["BTCUSD"]["opero"][i] == 1:
                close = datos["BTCUSD"]["close"][i]
                tomorrow = datos["BTCUSD"]["tomorrow"][i]
                acierto = datos["BTCUSD"]["acierto"][i]
                monto = operacion_diaria_btcusd(monto=monto_disponible_por_operacion, close=close,
                                                tomorrow=tomorrow, acierto=acierto)
                acumulado_montos.append(monto)

        if existe["EURUSD"]:
            if datos["EURUSD"]["opero"][i] == 1:
                close = datos["EURUSD"]["close"][i]
                tomorrow = datos["EURUSD"]["tomorrow"][i]
                acierto = datos["EURUSD"]["acierto"][i]
                monto = operacion_diaria_eurusd(monto=monto_disponible_por_operacion, close=close,
                                                tomorrow=tomorrow, acierto=acierto, total_operaciones=operaciones)
                acumulado_montos.append(monto)

        if existe["XAUUSD"]:
            if datos["XAUUSD"]["opero"][i] == 1:
                close = datos["XAUUSD"]["close"][i]
                tomorrow = datos["XAUUSD"]["tomorrow"][i]
                acierto = datos["XAUUSD"]["acierto"][i]
                monto = operacion_diaria_xauusd(monto=monto_disponible_por_operacion, close=close,
                                                tomorrow=tomorrow, acierto=acierto, total_operaciones=operaciones)
                acumulado_montos.append(monto)

        if existe["SPX"]:
            if datos["SPX"]["opero"][i] == 1:
                close = datos["SPX"]["close"][i]
                tomorrow = datos["SPX"]["tomorrow"][i]
                acierto = datos["SPX"]["acierto"][i]
                monto = operacion_diaria_spx(monto=monto_disponible_por_operacion, close=close,
                                             tomorrow=tomorrow, acierto=acierto, total_operaciones=operaciones)
                acumulado_montos.append(monto)

        monto_final_dia = 0
        for i in range(operaciones):
            monto_final_dia += acumulado_montos[i]

        montos_fin_dia.append(monto_final_dia)

    df = df.with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ])
    return df
