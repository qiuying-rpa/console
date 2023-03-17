import os
import time
from pathlib import Path

from flask import current_app as app, render_template, request
from utils.gen_code import generate_python_code


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/run')
def run_process():
    folder_path = Path('scripts')
    folder_path.mkdir(exist_ok=True)
    script_path = folder_path / f'{time.time()}.py'
    json = request.get_json()
    with open(script_path, 'wt', encoding='utf-8') as f:
        f.writelines(generate_python_code(json))
    os.system('python '+script_path.as_posix())
    return ''
