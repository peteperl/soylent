from flask import Flask
from flask import render_template
from flask import request
import json
import soylent

app = Flask(__name__)


@app.route('/')
def index():
    res = soylent.getSoyRainAll(8)
    return render_template('index.html', results=res)


@app.route('/', methods=['POST'])
def results():
    if soylent.validateState(request.form['state']):
        res = soylent.getSoyRainState(4, request.form['state'])
        return render_template('output.html', results=res, state=request.form['state'])
    else:
        res = [request.form['state'], request.form['state']]
        return render_template('bad.html', results=res)


@app.route('/lookup')
def lookup():
    return render_template('lookup.html')


@app.route('/lookup/', methods=['POST'])
def lookupoutput():
    # return json.dumps([request.form['state'], request.form['county']])
    # return json.dumps(res)
    if soylent.validateCounty(request.form['state'], request.form['county']):
        res = soylent.get_soyrain(request.form['state'], request.form['county'])
        return render_template('outputl.html', results=res)
    else:
        res = [request.form['state'], request.form['county']]
        return render_template('bad.html', results=res)


@app.route('/mockres')
def mockres():
    res = soylent.soyrain_mock()
    return render_template('output.html', results=res)

@app.route('/mocktext')
def mocktext():
    res = soylent.soyrain_mock()
    return json.dumps(res)

@app.route('/test')
def test():
    return 'Test a route: Success!!'

@app.route('/testlist')
def testlist():
    your_list = [1,2,3,4]
    return render_template('testlist.html', your_list=your_list)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run()
