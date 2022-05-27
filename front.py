from dash import Dash, html, dcc

instruments = [f'ticker_{i:02d}' for i in range(100)]

app = Dash(__name__)
app.title = 'Test. Python'

app.layout = html.Div(children=[
    html.H1(children='Chart'),

    html.Div(children='Select trading instrument:'),

    html.Div(
        [
            dcc.Dropdown(instruments, instruments[0], clearable=False)
        ], style={"width": '15%'})
])

if __name__ == '__main__':
    app.run(debug=True)