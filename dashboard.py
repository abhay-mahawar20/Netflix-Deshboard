import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc

# Load and prepare data
df = pd.read_csv('netflix_titles.csv')

# Data cleaning
df = df.drop_duplicates()
df['country'] = df['country'].fillna('Unknown')
df['director'] = df['director'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Unknown')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year

# Calculate metrics
total_content = len(df)
total_movies = (df['type'] == 'Movie').sum()
total_shows = (df['type'] == 'TV Show').sum()
avg_year = int(df['release_year'].mean())
most_common_genre = df['listed_in'].dropna().str.split(', ').explode().value_counts().index[0]
total_countries = df['country'].nunique()

content_type = df['type'].value_counts()
top_countries = df['country'].value_counts().head(10)
top_genres = df['listed_in'].dropna().str.split(', ').explode().value_counts().head(10)
yearly = df['year_added'].dropna().value_counts().sort_index()

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define colors
colors = {
    'background': '#f8f9fa',
    'text': '#333333',
    'primary': '#4C78A8',
    'secondary': '#F58518',
    'success': '#54A24B',
    'danger': '#FF6B6B'
}

# Create KPI card function
def create_kpi_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title text-muted"),
            html.H2(str(value), style={'color': color, 'fontWeight': 'bold'})
        ]),
        style={'border': f'3px solid {color}', 'borderRadius': '10px'},
        className='mb-3'
    )

# Define app layout
app.layout = dbc.Container([
    html.Div(style={'backgroundColor': colors['background'], 'padding': '20px', 'borderRadius': '10px'}, children=[
        html.H1("Netflix Content Analysis Dashboard", className="text-center mb-4", style={'fontWeight': 'bold', 'color': colors['text']}),
        
        # KPI Cards Row
        dbc.Row([
            dbc.Col([create_kpi_card('Total Content', f"{total_content:,}", '#FF6B6B')], md=2),
            dbc.Col([create_kpi_card('Movies', f"{total_movies:,}", colors['primary'])], md=2),
            dbc.Col([create_kpi_card('TV Shows', f"{total_shows:,}", colors['secondary'])], md=2),
            dbc.Col([create_kpi_card('Avg Year', f"{avg_year}", colors['success'])], md=2),
            dbc.Col([create_kpi_card('Top Genre', most_common_genre, '#72B7B2')], md=2),
            dbc.Col([create_kpi_card('Countries', f"{total_countries}", '#E45756')], md=2),
        ], className="mb-4"),
        
        # Charts Row 1
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        x=content_type.index,
                        y=content_type.values,
                        labels={'x': 'Content Type', 'y': 'Count'},
                        title='Content Type Distribution',
                        color=content_type.index,
                        color_discrete_map={'Movie': colors['primary'], 'TV Show': colors['secondary']},
                        text=content_type.values
                    ).update_traces(textposition='outside', texttemplate='%{text:,.0f}').update_layout(
                        hovermode='x unified', template='plotly_white'
                    )
                )
            ], md=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        y=top_countries.index,
                        x=top_countries.values,
                        orientation='h',
                        labels={'x': 'Number of Titles', 'y': 'Country'},
                        title='Top 10 Countries',
                        color=top_countries.values,
                        color_continuous_scale='Blues',
                        text=top_countries.values
                    ).update_traces(textposition='outside', texttemplate='%{text:,.0f}').update_layout(
                        hovermode='y unified', template='plotly_white'
                    )
                )
            ], md=6),
        ], className="mb-4"),
        
        # Charts Row 2
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        x=range(len(top_genres)),
                        y=top_genres.values,
                        labels={'x': 'Genre', 'y': 'Count'},
                        title='Top 10 Genres',
                        color=top_genres.values,
                        color_continuous_scale='Greens',
                        text=top_genres.values
                    ).update_layout(
                        xaxis={'tickmode': 'linear', 'tick0': 0},
                        xaxis_ticktext=top_genres.index,
                        xaxis_tickvals=list(range(len(top_genres))),
                        hovermode='x unified',
                        template='plotly_white'
                    ).update_traces(textposition='outside', texttemplate='%{text:,.0f}')
                )
            ], md=8),
            dbc.Col([
                dcc.Graph(
                    figure=go.Figure(data=[
                        go.Scatter(
                            x=yearly.index,
                            y=yearly.values,
                            mode='lines+markers',
                            name='Titles Added',
                            line=dict(color='#E45756', width=3),
                            fill='tozeroy',
                            marker=dict(size=8)
                        )
                    ]).update_layout(
                        title='Content Added Over Years',
                        xaxis_title='Year',
                        yaxis_title='Count',
                        hovermode='x unified',
                        template='plotly_white'
                    )
                )
            ], md=4),
        ]),
    ]),
], fluid=True, style={'backgroundColor': colors['background']})

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050, host='127.0.0.1')
