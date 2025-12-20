from dash import html, dcc
from utils.utils import diccionario_drop


def returned_drop_component(deactive_tab: bool, value_drop: str):
    options = list(diccionario_drop.keys())
    color_placeholder = "rgb(143, 155, 163)" if deactive_tab else "rgb(255, 255, 255)"
    font_weight_placehold = "" if deactive_tab else "bold"
    
    drop_component = html.Div(
        [
            html.P("Select Combination", id="placeholder", style={"color": color_placeholder, "font-weight": font_weight_placehold} ),
            dcc.Dropdown(
                id="drop-down",
                placeholder="Combinación Instrumento/Librería",   
                disabled=deactive_tab,
                options=options,
                value=value_drop,
                style={
                    "fontSize": "0.9rem",
                    "color": "black",
                },
            ),
        ], id="placeholder-drop-dow"
    )
    return drop_component