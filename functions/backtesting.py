import polars as pl
from utils.utils import columnas_librerias


def determinar_librerias_con_modelo(df: pl.DataFrame) -> int:
    """ DETERMINA CUANTAS LIBRERIAS TIENEN MODELO PARA EL INSTRUMENTO (DEL DATAFRAME QUE RECIBE)"""
    if len(df.columns) <= 7:
        return 1
    columnas_estartegias = ["sklearn_estrategia", "lightgbm_estrategia", "xgboost_estrategia", "pytorch_estrategia", "tensorflow_estrategia"]
    librerias_sin_modelo = df.select([(pl.col(col) == "").cast(int).alias(col) for col in columnas_estartegias]).row(0)
    librerias_con_modelo = 5 - sum(librerias_sin_modelo)
    return librerias_con_modelo


def backtesting_btcusd(df: pl.DataFrame,
                       estrategia: str,
                       transaction_cost_pct: float = 0.002,
                       monto_inicial_portafolio: float = 10000.0,
                       numero_instrumentos_financieros: int = 4) -> pl.DataFrame:

    monto_disponible = monto_inicial_portafolio / numero_instrumentos_financieros
    librerias_con_modelo = determinar_librerias_con_modelo(df=df)
    prices = df["close"].to_list()
    prices_tomorrow = df["close_tomorrow"].to_list()

    trades_diarios = df["trades_dia"].to_list()
    wins_diarios = df["wins_dia"].to_list()
    montos_inicios_dia = []
    montos_fin_dia = []
    monto_final_dia = 0
    for i in range(len(prices)):
        if i == 0:
            montos_inicios_dia.append(monto_disponible)
        else:
            montos_inicios_dia.append(montos_fin_dia[i - 1])
            monto_disponible = montos_fin_dia[i - 1]

        trades = trades_diarios[i]
        wins = wins_diarios[i]
        losses = trades - wins

        # Si los Trades en Ambos Sentidos son Iguales Se van a anular, Ese dia no se Invierte y se ahorran los costos
        if (trades == 0) or (wins == losses):
            montos_fin_dia.append(monto_disponible)
            continue

        # *******************************************************************************************************
        cambio_porcentual = abs((prices_tomorrow[i] - prices[i]) / prices[i])
        monto_disponible_X_operacion = 0
        if estrategia == "INDIVIDUAL":
            monto_disponible_X_operacion = round((monto_disponible / librerias_con_modelo), 2)
        elif estrategia == "MAYORIA_PONDERADA":
            monto_disponible_X_operacion = round((monto_disponible / trades), 2)
        else:
            monto_disponible_X_operacion = monto_disponible

        if wins > losses:
            numero_operaciones_dia = 1 if (estrategia == "MAYORIA_ESTRICTA") else (wins - losses)
            ganancia = (monto_disponible_X_operacion * cambio_porcentual) * numero_operaciones_dia
            costo_operaciones = numero_operaciones_dia * monto_disponible_X_operacion * transaction_cost_pct
            monto_final_dia = monto_disponible + ganancia - costo_operaciones
            montos_fin_dia.append(monto_final_dia)
            continue

        # EN CASO DE QUE LOS NO_ACIERTOS SEAN > A LOS ACIERTOS
        if losses > wins:
            numero_operaciones_dia = 1 if (estrategia == "MAYORIA_ESTRICTA") else (losses - wins)
            perdida = (monto_disponible_X_operacion * cambio_porcentual) * numero_operaciones_dia
            costo_operaciones = numero_operaciones_dia * monto_disponible_X_operacion * transaction_cost_pct
            monto_final_dia = monto_disponible - perdida - costo_operaciones
            montos_fin_dia.append(monto_final_dia)

    df = df.select(["date", "close", "close_tomorrow", "trades_dia", "wins_dia"]).sort("date").with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ]).with_columns(pl.lit(f"BTCUSD {estrategia}"))

    return df


def backtesting_eurusd(df: pl.DataFrame,
                       estrategia: str,
                       transaction_cost_pips: float = 1.5,
                       lotaje: float = 1,
                       monto_inicial_portafolio: float = 10000.0,
                       numero_instrumentos_financieros: int = 4) -> pl.DataFrame:
    librerias_con_modelo = determinar_librerias_con_modelo(df=df)
    monto_disponible = monto_inicial_portafolio / numero_instrumentos_financieros
    prices = df["close"].to_list()
    prices_tomorrow = df["close_tomorrow"].to_list()
    trades_diarios = df["trades_dia"].to_list()
    wins_diarios = df["wins_dia"].to_list()
    montos_inicios_dia = []
    montos_fin_dia = []
    monto_final_dia = 0

    for i in range(len(prices)):
        if i == 0:
            montos_inicios_dia.append(monto_disponible)
        else:
            montos_inicios_dia.append(montos_fin_dia[i - 1])
            monto_disponible = montos_fin_dia[i - 1]

        trades = trades_diarios[i]
        wins = wins_diarios[i]
        losses = trades - wins

        if (trades == 0) or (wins == losses):
            montos_fin_dia.append(monto_disponible)
            continue

        lotaje_por_operacion = 0
        variacion_pips = round(abs(prices_tomorrow[i] - prices[i]), 4) * 10000
        if estrategia == "INDIVIDUAL":
            lotaje_por_operacion = round((lotaje / librerias_con_modelo), 2)
        elif estrategia == "MAYORIA_PONDERADA":
            lotaje_por_operacion = round((lotaje / trades), 2)
        else:
            lotaje_por_operacion = lotaje

        # EN CASO DE QUE TODAS LAS ACERTADAS SEAN > A LAS OPERACIONES FRACASADAS
        if wins > losses:
            numero_operaciones_dia = 1 if (estrategia == "MAYORIA_ESTRICTA") else (wins - losses)
            valor_pip = (10 * lotaje_por_operacion) * numero_operaciones_dia
            pips_ganancia = variacion_pips - transaction_cost_pips
            ganancia = valor_pip * pips_ganancia
            monto_final_dia = monto_disponible + ganancia
            montos_fin_dia.append(monto_final_dia)
            continue

        if losses > wins:
            numero_operaciones_dia = 1 if (estrategia == "MAYORIA_ESTRICTA") else (losses - wins)
            valor_pip = (10 * lotaje_por_operacion) * numero_operaciones_dia
            pips_perdida = variacion_pips + transaction_cost_pips
            perdida = valor_pip * pips_perdida
            monto_final_dia = monto_disponible - perdida
            montos_fin_dia.append(monto_final_dia)

    df = df.select(["date", "close", "close_tomorrow", "trades_dia", "wins_dia"]).sort("date").with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ]).with_columns(pl.lit(f"EURUSD {estrategia}"))

    return df


def backtesting_xauusd(df: pl.DataFrame,
                       estrategia: str,
                       transaction_cost_onza_controlada: float = 0.37,
                       lotaje: float = 0.1,
                       monto_inicial_portafolio: float = 10000.0,
                       numero_instrumentos_financieros: int = 4) -> pl.DataFrame:
    librerias_con_modelo = determinar_librerias_con_modelo(df=df)
    monto_disponible = monto_inicial_portafolio / numero_instrumentos_financieros
    prices = df["close"].to_list()
    prices_tomorrow = df["close_tomorrow"].to_list()
    trades_diarios = df["trades_dia"].to_list()
    wins_diarios = df["wins_dia"].to_list()
    montos_inicios_dia = []
    montos_fin_dia = []
    monto_final_dia = 0

    for i in range(len(prices)):
        if i == 0:
            montos_inicios_dia.append(monto_disponible)
        else:
            montos_inicios_dia.append(montos_fin_dia[i - 1])
            monto_disponible = montos_fin_dia[i - 1]

        trades = trades_diarios[i]
        wins = wins_diarios[i]
        losses = trades - wins

        if (trades == 0) or (wins == losses):
            montos_fin_dia.append(monto_disponible)
            continue

        lotaje_por_operacion = 0
        variacion_precio = abs(prices_tomorrow[i] - prices[i])
        if estrategia == "INDIVIDUAL":
            lotaje_por_operacion = round((lotaje / librerias_con_modelo), 2)
        elif estrategia == "MAYORIA_PONDERADA":
            lotaje_por_operacion = round((lotaje / trades), 2)
        else:
            lotaje_por_operacion = lotaje

        # EN CASO DE QUE TODAS LAS ACERTADAS SEAN > A LAS OPERACIONES NO ACERTADAS
        if wins > losses:
            numero_operaciones_dia = 1 if (estrategia == "MAYORIA_ESTRICTA") else (wins - losses)
            lotaje_operaciones_dia = lotaje_por_operacion * numero_operaciones_dia
            onzas_controladas = lotaje_operaciones_dia * 100
            costo_operacion = transaction_cost_onza_controlada * onzas_controladas
            ganancia = variacion_precio * onzas_controladas
            monto_final_dia = monto_disponible + ganancia - costo_operacion
            montos_fin_dia.append(monto_final_dia)
            continue

        # EN CASO DE QUE TODAS LAS NO ACERTADAS SEAN > A LAS OPERACIONES ACERTADAS
        if losses > wins:
            numero_operaciones_dia = 1 if (estrategia == "MAYORIA_ESTRICTA") else (losses - wins)
            lotaje_operaciones_dia = lotaje_por_operacion * numero_operaciones_dia
            onzas_controladas = lotaje_operaciones_dia * 100
            costo_operacion = transaction_cost_onza_controlada * onzas_controladas
            perdida = variacion_precio * onzas_controladas
            monto_final_dia = monto_disponible - perdida - costo_operacion
            montos_fin_dia.append(monto_final_dia)
            continue

    df = df.select(["date", "close", "close_tomorrow", "trades_dia", "wins_dia"]).sort("date").with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ]).with_columns(pl.lit(f"XAUUSD {estrategia}"))

    return df


def backtesting_spx(df: pl.DataFrame,
                    estrategia: str,
                    transaction_total_cost_lote: float = 12,
                    lotaje: float = 1,
                    monto_inicial_portafolio: float = 10000.0,
                    numero_instrumentos_financieros: int = 4) -> pl.DataFrame:
    DOLARES_LOTAJE_X_PUNTO_BROKER_CFD = 10
    librerias_con_modelo = determinar_librerias_con_modelo(df=df)
    monto_disponible = monto_inicial_portafolio / numero_instrumentos_financieros

    puntos_iniciales_list = df["close"].to_list()
    puntos_finales_list = df["close_tomorrow"].to_list()
    trades_diarios = df["trades_dia"].to_list()
    wins_diarios = df["wins_dia"].to_list()
    montos_inicios_dia = []
    montos_fin_dia = []
    monto_final_dia = 0

    for i in range(len(puntos_iniciales_list)):
        if i == 0:
            montos_inicios_dia.append(monto_disponible)
        else:
            montos_inicios_dia.append(montos_fin_dia[i - 1])
            monto_disponible = montos_fin_dia[i - 1]

        trades = trades_diarios[i]
        wins = wins_diarios[i]
        losses = trades - wins

        if (trades == 0) or (wins == losses):
            montos_fin_dia.append(monto_disponible)
            continue

        variacion_puntos = abs(puntos_finales_list[i] - puntos_iniciales_list[i])
        if estrategia == "INDIVIDUAL":
            lotaje_por_operacion = round((lotaje / librerias_con_modelo), 2)
        elif estrategia == "MAYORIA_PONDERADA":
            lotaje_por_operacion = round((lotaje / trades), 2)
        else:
            lotaje_por_operacion = lotaje

        # EN CASO DE QUE TODAS LAS ACERTADAS SEAN > A LAS OPERACIONES NO ACERTADAS
        if wins > losses:
            numero_operaciones_dia = 1 if (estrategia == "MAYORIA_ESTRICTA") else (wins - losses)
            lotaje_operaciones_dia = lotaje_por_operacion * numero_operaciones_dia
            costo_operacion = transaction_total_cost_lote * lotaje_operaciones_dia
            ganancia = variacion_puntos * DOLARES_LOTAJE_X_PUNTO_BROKER_CFD * lotaje_operaciones_dia
            monto_final_dia = monto_disponible + ganancia - costo_operacion
            montos_fin_dia.append(monto_final_dia)
            continue

        # EN CASO DE QUE TODAS LAS NO ACERTADAS SEAN > A LAS OPERACIONES ACERTADAS
        if losses > wins:
            numero_operaciones_dia = 1 if (estrategia == "MAYORIA_ESTRICTA") else (losses - wins)
            lotaje_operaciones_dia = lotaje_por_operacion * numero_operaciones_dia
            costo_operacion = transaction_total_cost_lote * lotaje_operaciones_dia
            perdida = variacion_puntos * DOLARES_LOTAJE_X_PUNTO_BROKER_CFD * lotaje_operaciones_dia
            monto_final_dia = monto_disponible - perdida - costo_operacion
            montos_fin_dia.append(monto_final_dia)
            continue

    df = df.select(["date", "close", "close_tomorrow", "trades_dia", "wins_dia"]).sort("date").with_columns([
        pl.Series(name="Monto_ini_dia", values=montos_inicios_dia),
        pl.Series(name="Monto_fin_dia", values=montos_fin_dia)
    ]).with_columns(pl.lit(f"SPX {estrategia}"))

    return df


def evolucion(df_btc: pl.DataFrame, df_eur: pl.DataFrame, df_xau: pl.DataFrame, df_spx: pl.DataFrame) -> pl.DataFrame:
    minisymbols = ["btc", "eur", "xau", "spx"]
    dfs = [df_btc, df_eur, df_xau, df_spx]
    for i, symbol in enumerate(minisymbols):
        dfs[i] = dfs[i].drop(["close", "close_tomorrow", "trades_dia", "wins_dia", "literal"]).rename({
            "Monto_ini_dia": f"{symbol}_Monto_ini",
            "Monto_fin_dia": f"{symbol}_Monto_fin",
        })
    df_evolucion_capital = (
        dfs[0].join(dfs[1], on="date", how="left", coalesce=True)
        .join(dfs[2], on="date", how="left", coalesce=True)
        .join(dfs[3], on="date", how="left", coalesce=True)
    ).fill_null(strategy="forward").sort("date")

    columns_Monto_ini = [x for x in df_evolucion_capital.columns if "Monto_ini" in x]
    columns_Monto_fin = [x for x in df_evolucion_capital.columns if "Monto_fin" in x]

    df_evolucion_capital = df_evolucion_capital.with_columns([
        pl.sum_horizontal(columns_Monto_ini).alias("Monto_ini"),
        pl.sum_horizontal(columns_Monto_fin).alias("Monto_fin"),
    ])
    return df_evolucion_capital


def trades(inferencias_btc: pl.DataFrame, inferencias_eur: pl.DataFrame, inferencias_xau: pl.DataFrame, inferencias_spx: pl.DataFrame) -> pl.DataFrame:
    dfs = [inferencias_btc, inferencias_eur, inferencias_xau, inferencias_spx]
    minisymbols = ["btc", "eur", "xau", "spx"]
    for i, symbol in enumerate(minisymbols):
        dfs[i] = dfs[i].select(["date", "trades_dia", "wins_dia", "mayoria_estricta_trade", "mayoria_estricta_win"])
        dfs[i].columns = ["date", f"{symbol}_trades", f"{symbol}_wins", f"{symbol}_mayoria_trades", f"{symbol}_mayoria_wins"]

    df_trades = (
        dfs[0].join(dfs[1], on="date", how="left", coalesce=True)
        .join(dfs[2], on="date", how="left", coalesce=True)
        .join(dfs[3], on="date", how="left", coalesce=True)
    ).fill_null(strategy="zero")

    columns_trades = [x for x in df_trades.columns if "trades" in x]
    columns_wins = [x for x in df_trades.columns if "wins" in x]
    columns_trades_may = [x for x in df_trades.columns if ("trades" in x) and ("mayoria" not in x)]
    columns_wins_may = [x for x in df_trades.columns if ("wins" in x) and ("mayoria" not in x)]

    df_trades = df_trades.with_columns([
        pl.sum_horizontal(columns_trades).alias("Portafolio Trades"),
        pl.sum_horizontal(columns_wins).alias("Portafolio Wins"),
        pl.sum_horizontal(columns_trades_may).alias("Portafolio Trades Mayoria"),
        pl.sum_horizontal(columns_wins_may).alias("Portafolio Wins Mayoria"),
    ])

    return df_trades


# def portafolio_values(df_btc: pl.DataFrame, df_eur: pl.DataFrame, df_xau: pl.DataFrame, df_spx: pl.DataFrame) -> tuple[pl.DataFrame, dict]:
#     """Hubo que generar 2 Df Distintos y luego Juntarlos.
#       Porque??   Las Estrategia para rellenar los Nulos despues del join debe ser `forward` para lo que son los montos diarios
#                  (evolución de capital), mientras que la estrategia para rellenar los trades y wins debio ser 'zero'
#      """

#     dias = df_btc.shape[0]
#     minisymbols = ["btc", "eur", "xau", "spx"]
#     dfs = [df_btc, df_eur, df_xau, df_spx]
#     dfs_trades = []
#     for i, symbol in enumerate(minisymbols):
#         dfs_trades.append(dfs[i].select(["date", "trades_dia", "wins_dia"]))
#         dfs[i] = dfs[i].drop(["close", "close_tomorrow", "trades_dia", "wins_dia", "literal"]).rename({
#             "Monto_ini_dia": f"{symbol}_Monto_ini",
#             "Monto_fin_dia": f"{symbol}_Monto_fin",
#         })
#         dfs_trades[i] = dfs_trades[i].rename({
#             "trades_dia": f"{symbol}_trades",
#             "wins_dia": f"{symbol}_wins",
#         })
#     # EVOLUCION CAPITAL
#     df_evolucion_capital = (
#         dfs[0].join(dfs[1], on="date", how="left", coalesce=True)
#         .join(dfs[2], on="date", how="left", coalesce=True)
#         .join(dfs[3], on="date", how="left", coalesce=True)
#     ).fill_null(strategy="forward").sort("date")

#     columns_Monto_ini = [x for x in df_evolucion_capital.columns if "Monto_ini" in x]
#     columns_Monto_fin = [x for x in df_evolucion_capital.columns if "Monto_fin" in x]

#     df_evolucion_capital = df_evolucion_capital.with_columns([
#         pl.sum_horizontal(columns_Monto_ini).alias("Monto_ini"),
#         pl.sum_horizontal(columns_Monto_fin).alias("Monto_fin"),
#     ])  # .drop(columns_Monto_ini).drop(columns_Monto_fin)

#     # TRADES DIARIOS
#     df_trades = (
#         dfs_trades[0].join(dfs_trades[1], on="date", how="left", coalesce=True)
#         .join(dfs_trades[2], on="date", how="left", coalesce=True)
#         .join(dfs_trades[3], on="date", how="left", coalesce=True)
#     ).fill_null(strategy="zero").sort("date")
#     columns_trades = [x for x in df_trades.columns if "trades" in x]
#     columns_wins = [x for x in df_trades.columns if "wins" in x]
#     df_trades = df_trades.with_columns([
#         pl.sum_horizontal(columns_trades).alias("Portafolio Trades"),
#         pl.sum_horizontal(columns_wins).alias("Portafolio Wins"),
#     ])  # .drop(columns_trades).drop(columns_wins)

#     df = df_trades.join(df_evolucion_capital, on="date", how="left", coalesce=True)

#     trades = df['Portafolio Trades'].sum()
#     wins = df['Portafolio Wins'].sum()
#     inicio = round((df["Monto_ini"][0]), 2)
#     fin = round((df["Monto_fin"][-1]), 2)
#     profit = round((((fin - inicio) / inicio) * 100), 2)

#     portafolio_metrics = {
#         "monto_inicial" : inicio,
#         "monto_final": fin,
#         "profit": profit,
#         "proyeccion_anual": round((profit / dias * 365), 2),
#         "trades": trades,
#         "wins": wins,
#         "winrate": round(100 * (wins / trades), 2) if trades != 0 else 0,
#         "dias": dias
#     }

#     return df, portafolio_metrics


def backtesting_especifico(df: pl.DataFrame, libreria: str, instrumento: str) -> pl.DataFrame:
    if df[f"{libreria}_estrategia"][0] == "":
        return pl.DataFrame()

    df = df.select(columnas_librerias[libreria])
    df.columns = ['date', 'close', 'close_tomorrow', 'pred', 'estrategia', 'trades_dia', 'wins_dia']

    df_back = pl.DataFrame()

    if instrumento == "btcusd":
        df_back = backtesting_btcusd(df=df, estrategia="MAYORIA_ESTRICTA", numero_instrumentos_financieros=1)
    elif instrumento == "eurusd":
        df_back = backtesting_eurusd(df=df, estrategia="MAYORIA_ESTRICTA", numero_instrumentos_financieros=1)
    elif instrumento == "xauusd":
        df_back = backtesting_xauusd(df=df, estrategia="MAYORIA_ESTRICTA", numero_instrumentos_financieros=1)
    else:
        df_back = backtesting_spx(df=df, estrategia="MAYORIA_ESTRICTA", numero_instrumentos_financieros=1)

    return df_back
