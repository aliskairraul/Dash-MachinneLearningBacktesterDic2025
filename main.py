from dash import Dash, dcc, html, Input, Output, callback, exceptions
import polars as pl
import dash_bootstrap_components as dbc
from datetime import datetime, timezone, timedelta
from components.component_drop import returned_drop_component
from components.component_radioitems import returned_radioitems_component
from components.component_fecha import returned_date_component

from functions.callbacks_cargarData_cerrarModal import cargar_data, cerrar_modal, marcar_datos_listos
from functions.callback_actualizar_componentes import actualizar_componentes

inicio_operaciones = datetime(2025, 8, 1).date()
hoy = datetime.now(timezone.utc).date()

# 🪟 Modal de carga
modal_loading = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Cargando Data")),
        dbc.ModalBody("Por favor espere mientras se carga la información..."),
    ],
    id="modal-loading",
    is_open=True,
    backdrop="static",
    keyboard=False,
    centered=True
)

# ⏱️ Intervalo para disparar la carga
interval_loader = dcc.Interval(id="interval-loader", interval=500, n_intervals=0, max_intervals=1)

# 📦 Store para guardar Data individualizada de cada sesion de Usuario
store_cargo_data_correctamente = dcc.Store(id="cargo-data-externa", data={"cargo_correctamente": False})
store_datos = dcc.Store(id="store-datos")
store_es_primera_carga = dcc.Store(id="store-primera-carga", data=True)
store_drop_value = dcc.Store(id="store-drop-value", data="")
store_ready = dcc.Store(id="store-ready")

# 🚀 App Dash
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Machinne Learning Trading BACKTESTER"
)
# server = app.server

app.layout = html.Div([
    modal_loading,
    interval_loader,
    store_datos,
    store_es_primera_carga,
    store_drop_value,
    store_ready,

    html.Div([
        html.Div(" 🧠 Machinne Learning Trading BACKTESTER", id="titulo-encabezado"),
        html.Div(id="area-drop")
    ], id="area-encabezado"),

    html.Div([
        html.Div([
            html.Div(returned_date_component(min_date=inicio_operaciones, max_date=hoy, id_componente="date-picker-single-ini", inicio=True), id="fecha-inicio"),
            html.Div(returned_date_component(min_date=inicio_operaciones, max_date=hoy, id_componente="date-picker-single-fin", inicio=False), id="fecha-fin")
        ],id="area-fechas"),
        returned_radioitems_component(),
    ], id="area-fechas-radioitems"),

    html.Div([
        html.Div([
            html.Div([
                html.Div("Portafolio Overview", id="titulo-portafolio-overview", className="titulo-cajones"),
                html.Div(id="grafico-portafolio-overview", className="primario-degradado"),
                html.Div(id="grafico-portafolio-evolucion"),
            ], id="izq-sup", className="cajones"),
            html.Div([
                html.Div("Performance", id="titulo-portafolio-rates", className="titulo-cajones"),
                html.Div(id="portafolio-rates", className="mini-cajones"),
                # html.Div(id="portafolio-anual", className="mini-cajones"),
            ], id="izq-inf", className="cajones"),
        ], id="area-trabajo-izq"),

        html.Div([
            html.Div([
                html.Div([
                    html.Div("Instrument Metrics", id="titulo-performance_metrics", className="titulo-cajones"),
                    html.Div([
                        html.Div([
                            html.Div("S&P 500", id="titulo-spx", className="titulo-cards"),
                            html.Div(id="card-spx", className="contenido-cards")
                        ], className="card-metric"),
                        html.Div([
                            html.Div("EURUSD", id="titulo-eurusd", className="titulo-cards"),
                            html.Div(id="card-eur", className="contenido-cards")
                        ], className="card-metric"),
                        html.Div([
                            html.Div("BTCUSD", id="titulo-btcusd", className="titulo-cards"),
                            html.Div(id="card-btc", className="contenido-cards")
                        ], className="card-metric"),
                        html.Div([
                            html.Div("XAUUSD", id="titulo-xauusd", className="titulo-cards"),
                            html.Div(id="card-xau", className="contenido-cards")
                        ], className="card-metric"),
                    ], id="cards-metrics", className="primario-degradado"),
                    html.Div(id="grafico-barras"),
                ], id="der-sup-1", className="cajones"),
                html.Div([
                    html.Div("Daily Equity Evolution", id="titulo-linechart", className="titulo-cajones"),
                    html.Div(id="grafico-linechart"),
                ],id="der-sup-2", className="cajones")
            ], id="area-der-sup"),
            html.Div([
                html.Div([
                    html.Div("Trades per Instrument", id="titulo-tabla-peq", className="titulo-cajones"),
                    html.Div(id="tabla-peq"),
                ], id="der-inf-1", className="cajones"),
                html.Div([
                    html.Div("Daily Transactions", id="titulo-tabla-gde", className="titulo-cajones"),
                    html.Div(id="tabla-gde"),
                ], id="der-inf-2", className="cajones")
            ], id="area-der-inf")
        ], id="area-trabajo-der")

    ], id="area-trabajo")
], id="area-app")

        
if __name__ == "__main__":
    app.run(debug=True)
