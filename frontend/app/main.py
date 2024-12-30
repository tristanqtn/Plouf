from flask import Flask, render_template
import plotly.graph_objs as go
import plotly.io as pio
import numpy as np
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_ADDRESS = os.getenv('BACKEND_ADDRESS')
BACKEND_PORT = os.getenv('BACKEND_PORT')

FRONTEND_VERSION = os.getenv('FRONTEND_VERSION', '1.0.0')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pools')
def pools():
    response = requests.get(f'http://{BACKEND_ADDRESS}:{BACKEND_PORT}/pool/all')
    return render_template('pools.html', data=response.json())

if __name__ == '__main__':
    print(f"Backend version: {FRONTEND_VERSION}")
    app.run(debug=True)

