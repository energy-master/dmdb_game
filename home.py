from dash import html, dcc
import dash 
from dash import callback, Input, Output
from dash.dependencies import Input, Output
from view_game import build_game
from over_view import OverviewPage
from view_bot_bm import *

from benchmarking import BenchmarkingPage
import dash_bootstrap_components as dbc
from dash_data import *

from common_components import *


application_data = None
benchmarking_obj = None


app = dash.Dash(external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])



def create_page_home(app_data):
    nav = create_navbar(app)
    layout = html.Div([
        
        nav
        
    ])
    return layout
    

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'), Input('url', 'search'),])



def display_page(pathname,search):
    global benchmarking_obj
    if pathname == '/overview':
        overViewPage = OverviewPage(application_data=application_data, app=app)
        return overViewPage.build_overview()
    if pathname == '/game':
        return build_game(application_data)
    if pathname == '/benchmarking': 
        if benchmarking_obj == None:
            benchmarking_obj = BenchmarkingPage(application_data=application_data, app=app)
        return benchmarking_obj.build_benchmarking_page()

    if pathname == '/view_bot_bm': 
        print (app)
        viewBotPage = ViewBotPage(application_data=application_data, app=app, bot_id=search.split('=')[-1])
        return viewBotPage.build_bot_page()
    else:

        # overViewPage = OverviewPage(application_data)
        return create_page_home(application_data)



# --- GLOBAL CALL BACKS ---

if __name__ == '__main__':
    
    #applicaiton data
    application_data = IDentData()
    application_data.GetOpIds()
    application_data.SetActiveOptimisation(optimisation_id=application_data.optimisation_ids[0])
    application_data.BuildFrameworkOverview()
  
    
    
    
    # run dashboard
    app.run(debug=True,port=4040)