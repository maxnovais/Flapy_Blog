# coding: utf-8
from app import app
from config import APP_HOST, APP_PORT

app.run(host=APP_HOST, port=APP_PORT, debug=True, use_reloader=True)
