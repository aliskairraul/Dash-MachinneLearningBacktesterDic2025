import polars as pl
from utils.utils import paths_data_github


def rellenar_librerias_faltantes_con_0(df: pl.DataFrame) -> pl.DataFrame:
    predictores = ["sklearn_01", "lightgbm_01", "xgboost_01", "pytorch_01", "tensorflow_01"]
    for predictor in predictores:
        if predictor in df.columns:
            continue

        columna_opero = predictor.replace("01", "opero")
        columna_acierto = predictor.replace("01", "acierto")
        columna_estrategia = predictor.replace("01", "estrategia")

        df = df.with_columns([
            pl.lit(0).alias(predictor),
            pl.lit("").alias(columna_estrategia),
            pl.lit(0).alias(columna_opero),
            pl.lit(0).alias(columna_acierto)
        ])
    df = df.with_columns([
        pl.sum_horizontal(pl.col(["sklearn_opero", "lightgbm_opero", "xgboost_opero", "pytorch_opero", "tensorflow_opero"])).alias("operaciones"),
        pl.sum_horizontal(pl.col(["sklearn_acierto", "lightgbm_acierto", "xgboost_acierto", "pytorch_acierto", "tensorflow_acierto"])).alias("aciertos")
    ])
    df = df.with_columns(
        pl.when(pl.col("operaciones") == 0)
        .then(pl.lit(0))
        .otherwise(pl.lit(1))
        .alias("hubo_operacion")
    )
    return df


def backtesting_btcusd(df: pl.DataFrame, transaction_cost_pct: float = 0.002, monto_inicial: float = 2500.0):
    df = rellenar_librerias_faltantes_con_0(df=df).sort("date")

    prices = df["close"].to_list()
    prices_tomorrow = df["close_tomorrow"].to_list()
    num_operaciones = df["operaciones"].to_list()
    num_aciertos = df["aciertos"].to_list()
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

        operaciones = num_operaciones[i]
        aciertos = num_aciertos[i]
        no_aciertos = operaciones - aciertos

        if operaciones == 0 or aciertos == no_aciertos:
            montos_fin_dia.append(monto_disponible)
            continue

        cambio_porcentual = abs((prices_tomorrow[i] - prices[i]) / prices[i])
        monto_disponible_X_operacion = round((monto_disponible / operaciones), 2)

        # EN CASO DE QUE LOS ACIERTOS SEAN > A LOS NO_ACIERTOS
        # EJEMPLO: Esto ocurre si hay dos operaciones SHORT y una LONG y la estrategia correcta es SHORT.  Al final se restan y es preferible hacer una sola
        #          operacion con el 1/3 del costo
        if aciertos > no_aciertos:
            dif_aciertos = aciertos - no_aciertos
            ganancia = dif_aciertos * monto_disponible_X_operacion * cambio_porcentual
            costo_operaciones = dif_aciertos * monto_disponible_X_operacion * transaction_cost_pct
            monto_final_dia = monto_disponible + ganancia - costo_operaciones
            montos_fin_dia.append(monto_final_dia)
            continue

        # EN CASO DE QUE LOS NO_ACIERTOS SEAN > A LOS ACIERTOS
        if no_aciertos > aciertos:
            dif_no_aciertos = no_aciertos - aciertos
            perdida = dif_no_aciertos * monto_disponible_X_operacion * cambio_porcentual
            costo_operaciones = dif_no_aciertos * monto_disponible_X_operacion * transaction_cost_pct
            monto_final_dia = monto_disponible - perdida - costo_operaciones
            montos_fin_dia.append(monto_final_dia)

    df = df.with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ])

    return df


def backtesting_eurusd(df: pl.DataFrame, transaction_cost_pips: float = 1.5, monto_inicial: float = 2500.0, lotaje: float = 0.25):
    df = rellenar_librerias_faltantes_con_0(df=df).sort("date")

    prices = df["close"].to_list()
    prices_tomorrow = df["close_tomorrow"].to_list()
    num_operaciones = df["operaciones"].to_list()
    num_aciertos = df["aciertos"].to_list()
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

        operaciones = num_operaciones[i]
        aciertos = num_aciertos[i]
        no_aciertos = operaciones - aciertos

        if operaciones == 0 or aciertos == no_aciertos:
            montos_fin_dia.append(monto_disponible)
            continue

        variacion_pips = round(abs(prices_tomorrow[i] - prices[i]), 4) * 10000

        # EN CASO DE QUE TODAS LAS ACERTADAS SEAN > A LAS OPERACIONES FRACASADAS
        if aciertos > no_aciertos:
            lotaje_operacion = round((((aciertos - no_aciertos) * lotaje) / operaciones), 2)
            valor_pip = 10 * lotaje_operacion
            pips_ganancia = variacion_pips - transaction_cost_pips
            ganancia = valor_pip * pips_ganancia
            monto_final_dia = monto_disponible + ganancia
            montos_fin_dia.append(monto_final_dia)
            continue

        if no_aciertos > aciertos:
            lotaje_operacion = round((((aciertos - no_aciertos) * lotaje) / operaciones), 2)
            valor_pip = 10 * lotaje_operacion
            pips_perdida = variacion_pips + transaction_cost_pips
            perdida = valor_pip * pips_perdida
            monto_final_dia = monto_disponible - perdida
            montos_fin_dia.append(monto_final_dia)

    df = df.with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ])

    return df


def backtesting_xauusd(df: pl.DataFrame, transaction_cost_onza_controlada: float = 0.37, monto_inicial: float = 2500.0, lotaje: float = 0.025):
    df = rellenar_librerias_faltantes_con_0(df=df).sort("date")

    prices = df["close"].to_list()
    prices_tomorrow = df["close_tomorrow"].to_list()
    num_operaciones = df["operaciones"].to_list()
    num_aciertos = df["aciertos"].to_list()
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

        operaciones = num_operaciones[i]
        aciertos = num_aciertos[i]
        no_aciertos = operaciones - aciertos

        if operaciones == 0 or aciertos == no_aciertos:
            montos_fin_dia.append(monto_disponible)
            continue

        variacion_precio = abs(prices_tomorrow[i] - prices[i])

        # EN CASO DE QUE TODAS LAS ACERTADAS SEAN > A LAS OPERACIONES NO ACERTADAS
        if aciertos > no_aciertos:
            lotaje_operacion = round((((aciertos - no_aciertos) * lotaje) / operaciones), 2)
            onzas_controladas = lotaje_operacion * 100
            costo_operacion = transaction_cost_onza_controlada * onzas_controladas
            ganancia = variacion_precio * onzas_controladas
            monto_final_dia = monto_disponible + ganancia - costo_operacion
            montos_fin_dia.append(monto_final_dia)
            continue

        # EN CASO DE QUE TODAS LAS NO ACERTADAS SEAN > A LAS OPERACIONES ACERTADAS
        if no_aciertos > aciertos:
            lotaje_operacion = round((((no_aciertos - aciertos) * lotaje) / operaciones), 2)
            onzas_controladas = lotaje_operacion * 100
            costo_operacion = transaction_cost_onza_controlada * onzas_controladas
            perdida = variacion_precio * onzas_controladas
            monto_final_dia = monto_disponible - perdida - costo_operacion
            montos_fin_dia.append(monto_final_dia)
            continue

    df = df.with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ])

    return df


def backtesting_spx(df: pl.DataFrame, transaction_total_cost_lote: float = 12, monto_inicial: float = 2500.0, lotaje: float = 0.25):
    DOLARES_LOTAJE_X_PUNTO_BROKER_CFD = 10
    df = rellenar_librerias_faltantes_con_0(df=df).sort("date")

    puntos_iniciales_list = df["close"].to_list()
    puntos_finales_list = df["close_tomorrow"].to_list()
    num_operaciones = df["operaciones"].to_list()
    num_aciertos = df["aciertos"].to_list()
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

        operaciones = num_operaciones[i]
        aciertos = num_aciertos[i]
        no_aciertos = operaciones - aciertos

        if operaciones == 0 or aciertos == no_aciertos:
            montos_fin_dia.append(monto_disponible)
            continue

        variacion_puntos = abs(puntos_finales_list[i] - puntos_iniciales_list[i])

        # EN CASO DE QUE TODAS LAS ACERTADAS SEAN > A LAS OPERACIONES NO ACERTADAS
        if aciertos > no_aciertos:
            lotaje_operacion = round((((aciertos - no_aciertos) * lotaje) / operaciones), 2)
            costo_operacion = transaction_total_cost_lote * lotaje_operacion
            ganancia = variacion_puntos * DOLARES_LOTAJE_X_PUNTO_BROKER_CFD * lotaje_operacion
            monto_final_dia = monto_disponible + ganancia - costo_operacion
            montos_fin_dia.append(monto_final_dia)
            continue

        # EN CASO DE QUE TODAS LAS NO ACERTADAS SEAN > A LAS OPERACIONES ACERTADAS
        if no_aciertos > aciertos:
            lotaje_operacion = round((((no_aciertos - aciertos) * lotaje) / operaciones), 2)
            costo_operacion = transaction_total_cost_lote * lotaje_operacion
            perdida = variacion_puntos * DOLARES_LOTAJE_X_PUNTO_BROKER_CFD * lotaje_operacion
            monto_final_dia = monto_disponible - perdida - costo_operacion
            montos_fin_dia.append(monto_final_dia)
            continue

    df = df.with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ])

    return df
