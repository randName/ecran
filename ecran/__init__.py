from threading import Event

from flask import Flask, json, request

from .canvas import Canvas

app = Flask(__name__)
app.config.from_envvar('ECRAN_SETTINGS')

Renderer = app.config['RENDERER']
size = app.config.get('SIZE', (1, 1))

halt = Event()
canvas = Canvas(size, halt=halt)
renderer = Renderer(canvas=canvas, halt=halt)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/send', methods=('POST',))
def send():
    resp = {'status': 'error'}
    data = request.get_json()
    name = data.pop('name')
    if name:
        print(name, data)

    return json.jsonify(resp)


@app.route('/shutdown')
def shutdown():
    halt.set()
    try:
        request.environ.get('werkzeug.server.shutdown')()
    except TypeError:
        pass
    return 'écran shut down'
