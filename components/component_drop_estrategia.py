from dash import html, dcc


def returned_drop_estrategia() -> html.Div:
    color_placeholder = "rgb(0, 0, 0)"
    font_weight_placehold = ""
    
    drop_component = html.Div(
        [
            html.P("Estrategias", id="place-estrategia", style={"color": color_placeholder, "font-weight": font_weight_placehold} ),
            dcc.Dropdown(
                id="drop-estrategias",
                placeholder="Estrategia Asignación Capital",   
                # disabled=deactive_tab,
                options=["Individual", "Mayoria Ponderada", "Mayoria Absoluta"],
                value="Mayoria Ponderada",
                style={
                    "fontSize": "0.9rem",
                    "color": "black",
                },
            ),
        ], id="component-drop-estrategia"
    )
    return drop_component