from dash import html, dcc
import polars as pl
from datetime import datetime, timedelta


def returned_date_component(min_date: datetime.date, max_date: datetime.date, id_componente: str, inicio: bool = True) -> html.Div:
    min_date = min_date if inicio else min_date + timedelta(days=7)
    max_date = max_date if not inicio else max_date - timedelta(days=7)
    fecha = min_date if inicio else max_date
    date_component = html.Div(
        [
            dcc.DatePickerSingle(
                id=id_componente,
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                initial_visible_month=min_date,
                date=fecha,
                style={
                    # "fontSize": "0.5rem",
                    "color": "black",
                    "border": "0px",
                    "backgroundColor": "transparent",
                },
                display_format='DD/MM/YYYY',
            ),
        ], id=f"container-{id_componente}"
    )
    return date_component
