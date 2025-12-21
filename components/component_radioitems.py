from dash import html, dcc


def returned_radioitems_component() -> html.Div:
    
    radioitem_component = html.Div(
        [
           dcc.RadioItems(
            id="dcc-radioitems",
            options=[
                # {"label": "All Models", "value": "all"},
                {"label": "Evolución Patrimonio (por Instrumentos)", "value": "instrumentos"},
                # {"label": "Portfolio & Librarys", "value": "librerias"},
                {"label": "Simulación Modelo Específico Vs Portafolio", "value": "opcion_drop"}
            ],
            className="my-radio-items",
            value="instrumentos",
            inline=True,
            style={
                    "fontSize": "1rem",
                    "color": "black",
                },
            # labelStyle={"display": "block"},    
            # inputStyle handled in CSS now 
           ) 
        ], id="radioitems"
    )
    return radioitem_component