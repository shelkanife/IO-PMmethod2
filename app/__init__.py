from flask import Flask, render_template, request
from app.mmethod import start
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Método de la M')


@app.route('/m-method', methods=['POST'])
def m_method():
    try:
        data_json = request.get_json()
        if "dataProblem" in data_json and "toSendProblem" in data_json:
            try:
                problem = json.loads(data_json['toSendProblem'])
                dataProblem = json.loads(data_json['dataProblem'])
                if isinstance(problem, list) and isinstance(dataProblem, list) and problem and dataProblem:
                    response = start(problem, dataProblem)
                    return json.dumps({"code": 200, "response": response})
            except json.JSONDecodeError as error:
                print(error)
        return json.dumps({"code": "501", "msg": "Error in data"})
    except TypeError:
        return json.dumps({"code": "501", "msg": "Error in data"})
