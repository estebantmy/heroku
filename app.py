
import dash
from dash import dcc, html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px

# Load the CSV files
df_distances = pd.read_csv('https://raw.githubusercontent.com/estebantmy/heroku/main/ottignies_distances.csv')
df_aed = pd.read_csv('https://raw.githubusercontent.com/estebantmy/heroku/main/AED_lovain.csv')

# Extract necessary columns for intervention points
lat_intervention = df_distances['Latitude intervention']
lon_intervention = df_distances['Longitude intervention']
distances = df_distances['Distance (km)']

# Extract necessary columns for AED locations
lat_aed = df_aed['latitude']
lon_aed = df_aed['longitude']
aed_addresses = df_aed['address']
public_availability = df_aed['public']

# Extract latitude and longitude for permanence points
lat_permanence = df_distances['Latitude permanence']
lon_permanence = df_distances['Longitude permanence']

# Create a DataFrame for intervention points
df_intervention = pd.DataFrame({
    'lat': lat_intervention,
    'lon': lon_intervention,
    'distance': distances
})

# Create a DataFrame for AED locations
df_aed_locations = pd.DataFrame({
    'lat': lat_aed,
    'lon': lon_aed,
    'address': aed_addresses,
    'public': public_availability
})

# Create a DataFrame for permanence points
df_permanence = pd.DataFrame({
    'lat': lat_permanence,
    'lon': lon_permanence
})

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Expose the server variable for Heroku

# Define a function to get color based on distance
def get_color(distance):
    if distance < 5:
        return '5km'
    elif 5 <= distance < 10:
        return '5-10km'
    else:
        return '>10km'

# Create a scatter mapbox figure
fig = px.scatter_mapbox(
    df_intervention,
    lat='lat',
    lon='lon',
    color=df_intervention['distance'].apply(get_color),
    size_max=15,
    zoom=12,
    mapbox_style='open-street-map',
    title='Intervention Points and AED Locations'
)

# Add AED locations to the map
for _, row in df_aed_locations.iterrows():
    fig.add_scattermapbox(
        lat=[row['lat']],
        lon=[row['lon']],
        mode='markers',
        marker=dict(
            size=20,
            color='green' if row['public'] == 'Y' else 'red'
        ),
        text=row['address'],
        name='AED Locations'
    )

# Add permanence points to the map
fig.add_scattermapbox(
    lat=df_permanence['lat'],
    lon=df_permanence['lon'],
    mode='markers',
    marker=dict(
        size=9,
        color='black',
    ),
    text='Permanence Location',
    name='Permanence Locations'
)

# Define the layout of the Dash app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Tabs([
                dcc.Tab(label='Small Map', children=[
                    dcc.Graph(figure=fig)
                ]),
                dcc.Tab(label='Image 1', children=[
                    html.Img(src='https://raw.githubusercontent.com/estebantmy/heroku/main/recommendations1.png', style={'width': '100%'})
                ]),
                dcc.Tab(label='Image 2', children=[
                    html.Img(src='https://raw.githubusercontent.com/estebantmy/heroku/main/recommendations2.png', style={'width': '100%'})
                ]),
                dcc.Tab(label='Image 3', children=[
                    html.Img(src='https://raw.githubusercontent.com/estebantmy/heroku/main/recommendations3.png', style={'width': '100%'})
                ]),
                dcc.Tab(label='Image 4', children=[
                    html.Img(src='https://raw.githubusercontent.com/estebantmy/heroku/main/recommendations4.png', style={'width': '100%'})
                ]),
                dcc.Tab(label='Image 5', children=[
                    html.Img(src='https://raw.githubusercontent.com/estebantmy/heroku/main/recommendations5(1).png', style={'width': '100%'})
                ]),
                dcc.Tab(label='Image 6', children=[
                    html.Img(src='https://raw.githubusercontent.com/estebantmy/heroku/main/zoom_in5.png', style={'width': '100%'})
                ]),
            ])
        ], width=12)
    ])
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
