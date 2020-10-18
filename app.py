import dash 
import dash_table
import dash_core_components as dcc
import dash_html_components as html

from finder import meta
from dash.exceptions import PreventUpdate
from dash.dependencies import Output, Input, State
from finder import search
from load_files import clean_text

app = dash.Dash(
	__name__
)

app.title = 'What video did he say that in?'
app.layout = html.Div([
    html.H1('Hey, in which video did Exurb1a say ____?'),
    html.Div(
        [
            dcc.Input(id='searchbar', type='text', value='Wizard Jizz'),
            html.Button('Search', id='searchbutton')
        ]
    ), 
    html.P('', id='exact'),
    dash_table.DataTable(
        id='search_results',
        columns=[
            {'name': 'Title', 'id': 'title'},
            {'name': 'URL', 'id': 'url', 'presentation': 'markdown'},
        ],
        data=[]
    )
])

### HELPERS ###
def urlify(s):
    s = 'https://www.youtube.com/' + s
    return '[%s](%s)' % (s,s)

### CALLBACKS ###
@app.callback(
    [Output('search_results', 'data'),
     Output('exact', 'children')],
    [Input('searchbutton', 'n_clicks')],
    [State('searchbar', 'value')]
)
def vid_search(junk, search_term):
    if search_term == None:
        raise PreventUpdate

    search_result = search(clean_text(search_term))
    ret = []
    resp_str = ''

    if len(search_result['exact']):
        for u in search_result['exact']:
            m = meta[u]
            ret.append({'title': m['title'], 'url': urlify(u)})
    
        resp_str = '"%s" is said in:' % search_term

    elif len(search_result['potential']):   
        p = search_result['potential'] 
        for i in range(len(p)):
            t = meta[p[i][1]]['title']
            u = p[i][1]
            ret.append({'title': t, 'url': urlify(u)})
        
        resp_str = "I didn't find an exact match, but these are pretty close:"
    
    else:
        resp_str = "Sorry, couldn't find a video where he said anything like that"
    
    return ret, resp_str

server = app.server 

######## START EVERYTHING ########    
if __name__ == '__main__':
	app.run_server(debug=True, use_reloader=True,  dev_tools_hot_reload=True)