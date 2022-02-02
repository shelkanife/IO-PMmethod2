from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',title='Método de la M')

@app.route('/m-method',methods=['POST'])
def m_method():
    ...