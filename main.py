from flask import Flask, flash, redirect, url_for, render_template, request
import pandas as pd
import os
from PassivePySrc import PassivePy
from werkzeug.utils import secure_filename



spacy_model = "en_core_web_sm"
passivepy = PassivePy.PassivePyAnalyzer(spacy_model)
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_column_name_in_df(df, column_name):
    df_columns = list(df.columns)
    if column_name not in df_columns:
        flash (f"Please enter the right column name. No {column_name} found.")
        return render_template('passivepy_page.html')

def read_file(filename, file_path):
    if filename.rsplit('.', 1)[1].lower() == 'csv':
        df = pd.read_csv(file_path)
    elif filename.rsplit('.', 1)[1].lower() == 'xlsx':
        df = pd.read_excel(file_path)
    return df

def save_file(file, filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return file_path


        

        
def analyze_dataset(mode, file, column_name):

    if file and allowed_file(file.filename):

        # get it from the user
        filename = secure_filename(file.filename)
        file_path = save_file(file, filename)

        df = read_file(filename, file_path)
        df.dropna(inplace=True)
        check_column_name_in_df(df, column_name)

        # do the analysis
        if mode=='corpus_level':
            df_output = passivepy.match_corpus_level(df=df, column_name = column_name, n_process = 1, batch_size = 50)
        elif mode=='sentence_level':
            df_output = passivepy.match_sentence_level(df=df, column_name = column_name, n_process = 1, batch_size = 50)

        # give it back to user
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv') 
        df_output.to_csv(output_path, index=False)

        return df_output
        

@app.route('/', methods=['POST', 'GET'])
def passivepy_page(mode='', **kwargs):

    # sample sentence ----------------------------------------------------------------
    if request.method == 'POST' and request.form['submit'] == "Analyze sample":
        if not request.form["sent"]:
            flash('Please enter the sentence!')
            return redirect(url_for('passivepy_page'))

        sample_text = request.form["sent"]
        df_sample_text = passivepy.match_text(sample_text)
        
        return render_template("passivepy_page.html", mode='sample_text', zip=zip, 
                    column_names=df_sample_text.columns.values, row_data=list(df_sample_text.values.tolist()))       
    
    # corpus level----------------------------------------------------------------
    if request.method == 'POST' and request.form['submit'] == "Analyze corpus-level":
        mode = 'corpus_level'

        if not request.form["column_name"]:
            flash('Please enter the column name!')
            return render_template('passivepy_page.html')
        column_name = request.form["column_name"]


        if 'sample_df' not in request.files:
            flash ("No file")
            return render_template('passivepy_page.html')
        file= request.files['sample_df']

        df_output = analyze_dataset(mode=mode, file=file, column_name=column_name)


        return render_template("passivepy_page.html", mode=mode, zip=zip, 
        column_names=df_output.columns.values, row_data=list(df_output.values.tolist()))

    # sentence level -----------------------------------------------------------------------
    elif request.method == 'POST' and request.form['submit'] == "Analyze sentence-level":

        mode = 'sentence_level'
        if not request.form["column_name"]:
            flash('Please enter the column name!')
            return render_template('passivepy_page.html')
        column_name = request.form["column_name"]


        if 'sample_df' not in request.files:
            flash ("No file")
            return render_template('passivepy_page.html')
        file= request.files['sample_df']


        df_output = analyze_dataset(mode=mode, file=file, column_name=column_name)

        return render_template("passivepy_page.html", mode=mode, zip=zip, 
        column_names=df_output.columns.values, row_data=list(df_output.values.tolist()))
    
    # main page------------------------------------------------------------------
    else:
        return render_template('passivepy_page.html', mode='')



# config------------------------------------------------
UPLOAD_FOLDER = 'static/uploaded_files/'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '12345'

#------------------------------------------------------




