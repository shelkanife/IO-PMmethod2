from flask import Flask,render_template,request
from app.mmethod import start
import json

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',title='Método de la M')

@app.route('/m-method',methods=['POST'])
def m_method():
    data_json=request.get_json()
    problem=json.loads(data_json['toSendProblem'])
    dataProblem=json.loads(data_json['dataProblem'])
    response=start(problem,dataProblem)
    return json.dumps(response)