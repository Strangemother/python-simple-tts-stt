import os

from flask import Flask
from flask import render_template
from flask import request
from flask.json import jsonify
import say

ROOT =  os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route('/')
def hello():
    #p = os.path.join(ROOT, 'js_audio/index.html')
    js_app = os.path.join(ROOT, 'templates')
    return render_template('index.html')#, template_folder=js_app)

para = """"
We no longer think of chairs as technology; we just think of them as chairs. But there was a time when we hadn't worked out how many legs chairs should have, how tall they should be, and they would often 'crash' when we tried to use them.
"""

@app.route('/convert/', methods=['GET','POST'])
@app.route('/convert/<text>')
def convert(text=None):
    #p = os.path.join(ROOT, 'js_audio/index.html')
    if text is None:
        if request.method == 'POST':
            text = request.form['text']
    text= text or para
    data = say.main(text=text)
    data['text'] = text
    return jsonify(data)

app.run(debug=True)
