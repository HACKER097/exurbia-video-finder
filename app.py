import dash 
import dash_table
import dash_core_components as dcc
import dash_html_components as html

from dash.exceptions import PreventUpdate
from dash.dependencies import Output, Input, State
from finder import meta, search
from load_files import clean_text

RET_WIDTH = '75%'
OVERHANG = '25px'

app = dash.Dash(
	__name__
)
server = app.server 

app.title = 'What video did he say that in?'
app.layout = html.Div([
    html.A([
        html.Img(
            src=app.get_asset_url('ex_logo.png'),
            style={
                'width': '50px', 
                'height':'40px', 
                'position': 'fixed', 
                'top': '5px'
            }
        )],
        href='https://www.youtube.com/user/willunicycleforfood'
    ),
    html.Div([
        html.P('In which video did Exurb1a say'),
        dcc.Input(id='searchbar', 
            type='text', 
            value='', 
            debounce=True,
            style={
                'background-color': 'rgba(0,0,0,0)',
                'color': 'white',
                'border-style': 'solid',
                'border-width': '0px 0px 1px 0px',
                'border-color': 'white',
                'display': 'inline-block',
                'font-size': '25px',
                'width': '80%'
        }),
        html.P('?', style={'display': 'inline-block'}),
        html.P('', id='exact'),
        ], 
        id='search'
    ),
    html.Div([
        html.Div('', id='results', style={'font-size': '20px'})
    ],
        style={
            'width': RET_WIDTH,
            'margin-left': 'calc(25% / 2)',
            'text-align': 'center'
        }
    ),
    html.Div([
        html.A([
            html.Img(
                src=app.get_asset_url('github-icon.png'),
                style={'width': '100%', 'height': '100%'}
            )],
            href='https://github.com/zazyzaya/exurbia-video-finder'
        )],
        id='footer',
        style={
            'width': '50px',
            'height': '50px',
            'position': 'fixed',
            'bottom': '0'
        }
    )
])

### HELPERS ###
def urlify_markup(s):
    s = 'https://www.youtube.com/watch?v=' + s
    return '[%s](%s)' % (s,s)

def urlify_dash(text, href):
    url = 'https://www.youtube.com/watch?v=' + href
    return html.P(
        html.A(text, href=url, target='_blank')
    )

def embed_youtube(text, href):
    eref = href.replace('&t', '?start')[:-1] # change for embedded URL format
    url = 'https://www.youtube.com/embed/' + eref
    iframe = html.Iframe(
        src=url,
        width=560,
        height=315,
        style={
            'frameborder':0,
            'width':'min(75%, 560)',
            'height':'calc(var(width) * 0.5625)', # Correct aspect ratio for determined width
            'allow':"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
            'margin-left': OVERHANG,
            'margin-right': OVERHANG
        }
    )

    line = html.Div(
        style={
            'height': '1px',
            'width': '100%',
            'background-color': 'white',
            'display': 'inline-block',
            'margin-bottom': '25px',
            'margin-top': '20px'
        }
    )

    vid_and_title = html.Div(
        [urlify_dash(text, href), iframe],
        style={
            'display': 'inline-block',
            'margin': '0 auto',
            'text-align': 'left'
        }
    )

    return [vid_and_title, line]

### CALLBACKS ###
@app.callback(
    [Output('results', 'children'),
     Output('exact', 'children')],
    [Input('searchbar', 'value')]
)
def vid_search(search_term):
    if search_term == None:
        raise PreventUpdate

    if search_term == '':
        return [''], ''

    search_result = search(clean_text(search_term))
    ret = []
    resp_str = ''

    if len(search_result['exact']):
        for u in search_result['exact']:
            m = meta[u.split('&')[0]]
            t = m['title']
            ret += embed_youtube(t, u)
    
        resp_str = '"%s" is said in:' % search_term

    elif len(search_result['potential']):   
        p = search_result['potential'] 
        for i in range(len(p)):
            t = meta[p[i][1]]['title']
            u = p[i][1]
            ret += embed_youtube(t, u)
        
        resp_str = "I didn't find an exact match, but these are pretty close:"
    
    else:
        resp_str = "Sorry, couldn't find a video where he said anything like that"
    
    return ret[:-1], resp_str

######## START EVERYTHING ########    
if __name__ == '__main__':
	# Production mode
    app.run_server()

    # Debug mode
    #app.run_server(debug=True, dev_tools_hot_reload=True)