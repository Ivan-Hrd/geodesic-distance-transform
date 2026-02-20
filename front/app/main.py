import numpy as np
import requests
from dash import Dash, dcc, html, Input, Output, callback, State
import base64
import plotly.express as px
import dash_daq as daq
import os

backend_url: str = os.environ.get("BACKEND_URL", "http://localhost:8080")

app = Dash()

app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-file",
            children="Drag and drop an image (only .png files will be uploaded)",
            style={
                "border": "1px dashed",
                "padding": "20px",
                "textAlign": "center",
            },
            multiple=False,  
            enable_folder_selection=False,# forbid folder drag-and-drop
            accept=".png",
        ),
        html.Div(id="output-file-upload"),
        dcc.Upload(
            id="upload-mask",
            children="Drag and drop a mask (only .png files will be uploaded)",
            style={
                "border": "1px dashed",
                "padding": "20px",
                "textAlign": "center",
            },
            multiple=False,  
            enable_folder_selection=False,# forbid folder drag-and-drop
            accept=".png",
        ),
        html.Div(id="output-mask-upload"),
        html.Div([
            html.Button("Compute Geodesic Distance", id="send-btn"),
            daq.BooleanSwitch(id='numba-switch', on=False, label="Use numba", labelPosition="top"),
        ], style={"display": "flex", "alignItems": "center", "gap": "16px"}),
        dcc.Graph(id="show-computed-res"),
        html.H1('Benchmark'),
                dcc.Upload(
            id="upload-file-bench",
            children="Drag and drop an image (only .png files will be uploaded)",
            style={
                "border": "1px dashed",
                "padding": "20px",
                "textAlign": "center",
            },
            multiple=False,  
            enable_folder_selection=False,# forbid folder drag-and-drop
            accept=".png",
        ),
        html.Div(id="output-file-upload-bench"),
        dcc.Upload(
            id="upload-mask-bench",
            children="Drag and drop a mask (only .png files will be uploaded)",
            style={
                "border": "1px dashed",
                "padding": "20px",
                "textAlign": "center",
            },
            multiple=False,  
            enable_folder_selection=False,# forbid folder drag-and-drop
            accept=".png",
        ),
        html.Div(id="output-mask-upload-bench"),
        html.Div([
        daq.NumericInput(
            min=1,
            max=100,
            value=1,
            label="number of iterations",
            labelPosition="top",
            id="n_iterations"),
        daq.BooleanSwitch(id='numba-switch-bench', on=False, label="Use numba", labelPosition="top"),
        ], style={"display": "flex", "alignItems": "center", "gap": "16px"}),
        html.Button("Generate Benchmark", id="bench-btn"),
        dcc.Graph(id="show-bench-res"),

    ]
)


@callback(
    Output("output-file-upload", "children"),
    Input("upload-file", "contents"),
)
def update_output(contents):
    if contents:
        return html.Div(
            [
                html.H5(f"Uploaded image:"),
                html.Div(
                    [
                        html.Img(src=contents, style={"height": "100px", "margin": "5px"})
                    ]
                ),
            ]
        )

@callback(
    Output("output-mask-upload", "children"),
    Input("upload-mask", "contents"),
)
def update_mask_output(contents):
    if contents:
        return html.Div(
            [
                html.H5(f"Uploaded mask:"),
                html.Div(
                    [
                        html.Img(src=contents, style={"height": "100px", "margin": "5px"})
                    ]
                ),
            ]
        )

@callback(
    Output("show-computed-res", "figure"),
    Input("send-btn", "n_clicks"),
    State("upload-file", "contents"),
    State("upload-mask", "contents"),
    State("numba-switch", "on"),
    prevent_initial_call=True
)
def update_backend_output(n_clicks, base_contents, mask_contents, numba):
    if base_contents and mask_contents:
        img_bytes, img_type = _get_raw_bytes(base_contents)
        msk_bytes, msk_type = _get_raw_bytes(mask_contents)
        try:
            response = requests.post(
                f"{backend_url}/single_traitement?numba={numba}".lower(),
                files={
                    "img": ("img.png", img_bytes, img_type),
                    "msk": ("mask.png", msk_bytes, msk_type),
                }
            )
            json_obj = response.json()
            bytesList = base64.b64decode(json_obj["traitementList"])  
            distance_array = np.frombuffer(bytesList, dtype=np.float64).reshape(json_obj["shape"])
            fig = px.imshow(distance_array, color_continuous_scale="inferno",
                                    title=f"Geodesic Distance, computed in {json_obj["timeToExecute"]} seconds")
            return fig
        except Exception as e:
            print(f"Error for image: {str(e)}")
            return None

def _get_raw_bytes(content):
    # content is like "data:image/png;base64,AAAA..."
    content_type, b64_data = content.split(",", 1)
    content_type = content_type.split(":")[1].split(";")[0]  # "image/png"
    raw_bytes = base64.b64decode(b64_data)
    return raw_bytes, content_type

@callback(
    Output("show-bench-res", "figure"),
    Input("bench-btn", "n_clicks"),
    State("upload-file-bench", "contents"),
    State("upload-mask-bench", "contents"),
    State("numba-switch-bench", "on"),
    State("n_iterations", "value"),
    prevent_initial_call=True
)
def update_bench_output(n_clicks, base_contents, mask_contents, numba, n_iterations):
    if base_contents and mask_contents:
        img_bytes, img_type = _get_raw_bytes(base_contents)
        msk_bytes, msk_type = _get_raw_bytes(mask_contents)
        try:
            response = requests.post(
                f"{backend_url}/benchmark?numba={numba}&n_iterations={n_iterations}".lower(),
                files={
                    "img": ("img.png", img_bytes, img_type),
                    "msk": ("mask.png", msk_bytes, msk_type),
                }
            )
            json_obj = response.json()
            benchList = json_obj["benchResList"]
            print(benchList)
            fig = px.line(
                x=list(range(len(benchList))),
                y=benchList,
                labels={"x": "Index", "y": "Time (s)"}
            )
            fig.update_traces(mode='lines+markers')
            return fig
        except Exception as e:
            print(f"Error for image: {str(e)}")
            return None

@callback(
    Output("output-file-upload-bench", "children"),
    Input("upload-file-bench", "contents"),
)
def update_output_bench(contents):
    if contents:
        return html.Div(
            [
                html.H5(f"Uploaded image:"),
                html.Div(
                    [
                        html.Img(src=contents, style={"height": "100px", "margin": "5px"})
                    ]
                ),
            ]
        )

@callback(
    Output("output-mask-upload-bench", "children"),
    Input("upload-mask-bench", "contents"),
)
def update_mask_output_bench(contents):
    if contents:
        return html.Div(
            [
                html.H5(f"Uploaded mask:"),
                html.Div(
                    [
                        html.Img(src=contents, style={"height": "100px", "margin": "5px"})
                    ]
                ),
            ]
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False, use_reloader=False)