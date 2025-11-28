


import dash_bootstrap_components as dbc
import dash_html_components as html
import requests


def buildTitle(app=None):
    title = html.Div(
        className = 'title-div',
        children = [
            (html.Img(src=app.get_asset_url("img/go_.jpg"), height="70px",className="float-left")),
            (html.Img(src=app.get_asset_url("img/logo.png"), height="70px",className="float-left")),
           
            # html.H5('Powered by', className="float-left"),
            # html.H2('MARLIN ',  className="brahma-title"),
             html.H2('IDent Learn', className="float-left"),
        ]
        )

    return (title)

LOGO = "https://vixen.hopto.org/img/rsa_bl.png"

def create_navbar(app=None):
    # Create the Navbar using Dash Bootstrap Components
    navbar = dbc.NavbarSimple(
        
        children=[
        #     html.A(
        #     dbc.Row(
        #         [
        #             dbc.Col(html.Img(src=app.get_asset_url("img/logo.png"), height="30px")),
        #             # dbc.Col(dbc.NavbarBrand("Navbar", className="ml-2")),
        #         ],
        #         align="right",
                
        #     ),
        #     href="https://plot.ly",
        # ),
        dbc.DropdownMenu(
            nav=True,
            
            color="white",
            in_navbar=True,
            label="DATA", # Label given to the dropdown menu
            children=[
                # In this part of the code we create the items that will appear in the dropdown menu on the right
                # side of the Navbar.  The first parameter is the text that appears and the second parameter 
                # is the URL extension.
                dbc.DropdownMenuItem("Home", href='/'), # Hyperlink item that appears in the dropdown menu
                dbc.DropdownMenuItem(divider=True), # Divider item that appears in the dropdown menu 
                #dbc.DropdownMenuItem("Overview", href='/overview'), # Hyperlink item that appears in the dropdown menu
                # dbc.DropdownMenuItem("Page 3", href='/page-3'), # Hyperlink item that appears in the dropdown menu
                dbc.DropdownMenuItem("Benchmarking", href='/benchmarking'),
                #dbc.DropdownMenuItem("Live", href='/live'),
                
            ],
            className = "m1"
        )
            
        ],
        
        brand=buildTitle(app),  # Set the text on the left side of the Navbar
        brand_href="/",  # Set the URL where the user will be sent when they click the brand we just created "Home"
        sticky="top",  # Stick it to the top... like Spider Man crawling on the ceiling?
        color="black",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for light text)
        id = "my_nav"
    )

    return navbar

def viewRunURL(filename,run_id, bot_id, data):
    """viewRunURL _summary_

    :param filename: _description_
    :type filename: _type_
    :param run_id: _description_
    :type run_id: _type_
    """
    
    # 343_bm_343%_20140822_155039_000_m_001_p_001.flac.json
    path = f"https://marlin-network.hopto.org/marlin_live_data/dump/out/{run_id}"
    filename = f'{run_id}_bm_{run_id}%{filename}.json'
    # url = f'{path}/{filename}'
    

    if data == "energy":
        url = f'{path}/{bot_id}_activity.png'
        return url
    if data == "decisions":
        url = f'{path}/{run_id}_decisions.png'
        return url
    
    return -1

def viewBotURL(bot_id):
    
    # bot_id = 'vixen_bot652101253078_4_str'
    # str_filename = f'{bot_id}_str.json'
    # print ('https://marlin-network.hopto.org/ident/str/{str_filename}')
    # resp = requests.get('https://vixen.hopto.org/rs/ident_app/ident_gui/brahma/bot_structure.php?bot_id={bot_id}')
    url = f'https://vixen.hopto.org/rs/ident_app/ident_gui/brahma/bot_structure.php?bot_id={bot_id}'
    # bot_str = resp.json()
    # url=f'https://jsoncrack.com/widget?json={bot_str}'
    print (url)
    return url
