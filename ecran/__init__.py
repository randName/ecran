from threading import Event

from flask import Flask, json, request

from .canvas import Canvas
from .animation import animations

app = Flask(__name__)
app.config.from_envvar('ECRAN_SETTINGS')

Renderer = app.config['RENDERER']
r_kwargs = app.config.get('RENDERER_KWARGS', {})

size = app.config.get('SIZE', (1, 1))

halt = Event()
canvas = Canvas(size, halt=halt)
renderer = Renderer(canvas=canvas, halt=halt, **r_kwargs)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/shutdown')
def shutdown():
    halt.set()
    try:
        request.environ.get('werkzeug.server.shutdown')()
    except TypeError:
        pass
    return 'écran shut down'


class APIError(Exception):
    pass


@app.errorhandler(APIError)
def api_error(e):
    return json.jsonify({'status': 'error', 'message': str(e)})


@app.route('/canvas', methods=('POST', 'GET'))
def canvas_api():
    resp = {'status': 'ok'}

    if request.method == 'GET':
        resp['animations'] = tuple(str(a) for a in canvas.animations)
        return json.jsonify(resp)

    data = request.get_json()

    try:
        action = data.pop('action')
    except KeyError:
        raise APIError('no action specified')
    except AttributeError:
        raise APIError('no data received')

    name = data.pop('name', None)
    params = data.pop('params', {})

    if action == 'clear':
        canvas.clear()
    elif action == 'add':
        try:
            atype = data['type']
        except KeyError:
            raise APIError('no animation type specified')
        try:
            canvas.add(animations[atype](uid=name, **params))
        except KeyError:
            raise APIError("no animation '%s'" % atype)
        except TypeError:
            raise APIError('could not initalize')
    elif action == 'update':
        canvas.update(name, params)
    else:
        raise APIError('unrecognized action')

    return json.jsonify(resp)
