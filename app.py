import os
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.after_request
def agregar_cabeceras_seguridad(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response


@app.route('/')
def inicio():
    nombre = escape(request.args.get('nombre', 'Visitante'))
    return f"""
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>App DevSecOps Segura</title>
    </head>
    <body>
        <h1>Hola, {nombre}!</h1>
        <p>Aplicacion Flask endurecida en el pipeline DevSecOps.</p>
    </body>
    </html>
    """


if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')  # nosec B104
    port = int(os.environ.get('FLASK_PORT', '5000'))
    app.run(host=host, port=port, debug=False)