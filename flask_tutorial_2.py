from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", content='first page.')

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route('/passivepy', methods=['POST', 'GET'])
def get_sent():
    return render_template("passivepy.html")

@app.route('/<usr>')
def user(usr):
    return f'this is {usr}'


if __name__ == "__main__":
    app.run(debug=True)




# passivepy section



# then run this to import the package and create PassivePy
import pandas as pd
import os
pd.set_option('display.max_colwidth', None)
from PassivePySrc import PassivePy


spacy_model = "en_core_web_lg"
passivepy = PassivePy.PassivePyAnalyzer(spacy_model)



# Try changing the sentence below:
sample_text = 'She has been killed'
passivepy.match_text(sample_text)


