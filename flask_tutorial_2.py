
# passivepy section



# then run this to import the package and create PassivePy
import pandas as pd
import os
pd.set_option('display.max_colwidth', None)
from PassivePySrc import PassivePy


spacy_model = "en_core_web_lg"
passivepy = PassivePy.PassivePyAnalyzer(spacy_model)


from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", content='first page.')

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route('/passivepy_page', methods=['POST', 'GET'])
def passivepy_page(tables=None, titles=None):
    if request.method == 'POST':
        sample_text = request.form["sent"]
        df = passivepy.match_text(sample_text)
        #return f'this is the result: {sample_result}'
        return render_template('passivepy_page.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
        #return render_template('result.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
    else:
        return render_template('passivepy_page.html', tables='no_result', titles='no_titles')

@app.route('/result')
def result(tables, titles):
    return render_template('result.html', tables, titles)


if __name__ == "__main__":
    app.run(debug=True)





