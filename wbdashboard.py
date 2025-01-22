from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path         # File path operations

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load your processed DataFrame `mdf`
data_path=Path(r'D:\AllProjects\multi-modller\team1')
mdf = pd.read_csv(data_path / 'processed_mdf.csv')  # Save your DataFrame to CSV after processing

# Normalize columns for visualization
mdf['normalized_greeness'] = mdf['greeness'] / mdf['greeness'].max()
mdf['normalized_noise'] = mdf['noise'] / mdf['noise'].max()

# Layout of the dashboard
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H1("Multimodal Data Dashboard", className="text-center mt-3 mb-5"),
            ]
        ),
        dbc.Row(
            [
                # Cluster Map Section
                dbc.Col(
                    [
                        html.H4("Person and Vehicle Clusters", className="mt-3"),
                        dcc.Graph(id='cluster-map'),
                    ],
                    md=6
                ),
                # Heatmap Section
                dbc.Col(
                    [
                        html.H4("Greeness & Noise Levels Heatmap", className="mt-3"),
                        dcc.Graph(id='heatmap'),
                        dbc.Label("Select Heatmap Metric:"),
                        dcc.Dropdown(
                            id="heatmap-metric",
                            options=[
                                {'label': 'Greeness', 'value': 'normalized_greeness'},
                                {'label': 'Noise', 'value': 'normalized_noise'}
                            ],
                            value='normalized_greeness',
                            clearable=False,
                        ),
                    ],
                    md=6
                ),
            ]
        ),
        dbc.Row(
            [
                # Filter Histograms
                dbc.Col(
                    [
                        html.H4("Histogram Analysis", className="mt-5"),
                        dbc.Label("Select a Numerical Feature:"),
                        dcc.Dropdown(
                            id='histogram-feature',
                            options=[{'label': col, 'value': col} for col in [
                                'person', 'vehicles', 'brightness', 'greeness', 'noise'
                            ]],
                            value='brightness',
                            clearable=False,
                        ),
                        dcc.Graph(id='histogram'),
                    ],
                    md=6
                ),
                # Correlation Section
                dbc.Col(
                    [
                        html.H4("Correlation Analysis", className="mt-5"),
                        dbc.Label("Filter by Place:"),
                        dcc.Dropdown(
                            id='place-dropdown',
                            options=[{'label': place, 'value': place} for place in mdf['place_name'].unique()],
                            value=mdf['place_name'].unique()[0],
                            clearable=False,
                        ),
                        dcc.Graph(id='correlation-heatmap'),
                    ],
                    md=6
                ),
            ]
        ),
    ],
    fluid=True
)


# Callback for Cluster Map
@app.callback(
    Output('cluster-map', 'figure'),
    Input('heatmap-metric', 'value')
)
def update_cluster_map(metric):
    traces = []
    scaling_factor = 1000 / mdf['person'].max()
    for cluster in sorted(mdf['place_cluster'].unique()):
        cluster_data = mdf[mdf['place_cluster'] == cluster]
        traces.append(
            go.Scattermapbox(
                lat=cluster_data['lat'],
                lon=cluster_data['lon'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=cluster_data['person'] * scaling_factor,
                    sizemode='area',
                    sizeref=2. * scaling_factor / (40. ** 2),
                ),
                name=f"Place {cluster}",
            )
        )
    map_fig = go.Figure(traces)
    map_fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=mdf['lat'].mean(), lon=mdf['lon'].mean()),
            zoom=12
        ),
        height=500,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return map_fig


# Callback for Heatmap
@app.callback(
    Output('heatmap', 'figure'),
    Input('heatmap-metric', 'value')
)
def update_heatmap(metric):
    heatmap_fig = go.Figure(
        go.Densitymapbox(
            lat=mdf['lat'],
            lon=mdf['lon'],
            z=mdf[metric],
            radius=20,
            colorscale="Viridis",
            showscale=True,
        )
    )
    heatmap_fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=mdf['lat'].mean(), lon=mdf['lon'].mean()),
            zoom=12
        ),
        height=500,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return heatmap_fig


# Callback for Histogram
@app.callback(
    Output('histogram', 'figure'),
    Input('histogram-feature', 'value')
)
def update_histogram(feature):
    hist_fig = px.histogram(mdf, x=feature, nbins=20, title=f"Distribution of {feature}")
    return hist_fig


# Callback for Correlation Heatmap
@app.callback(
    Output('correlation-heatmap', 'figure'),
    Input('place-dropdown', 'value')
)
def update_corr_heatmap(place_name):
    place_data = mdf[mdf['place_name'] == place_name]
    corr_matrix = place_data.corr().round(3)
    heatmap_fig = px.imshow(
        corr_matrix,
        color_continuous_scale='coolwarm',
        title=f"Correlation Matrix for {place_name}",
    )
    return heatmap_fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
