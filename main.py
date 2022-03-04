from flask import Flask, flash, redirect, url_for, render_template, request
import pandas as pd
import os
from PassivePySrc import PassivePy
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


spacy_model = "en_core_web_sm"
passivepy = PassivePy.PassivePyAnalyzer(spacy_model)

# Flask ----------------------------------------------------------------
app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def passivepy_page(mode='', **kwargs):

    # sample sentence ----------------------------------------------------------------
    if request.method == 'POST' and request.form['submit'] == "Analyze sample":
        sample_text = request.form["sent"]
        df_sample_text = passivepy.match_text(sample_text)
        #return f'this is the result: '
        return render_template("passivepy_page.html", mode='sample_text', zip=zip, 
                    column_names=df_sample_text.columns.values, row_data=list(df_sample_text.values.tolist()))       
                     #return render_template('result.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
    
    # corpus level----------------------------------------------------------------
    if request.method == 'POST' and request.form['submit'] == "Analyze corpus-level":
        if not request.form["column_name_c"]:
            flash('Please enter the column name!')
            return redirect(url_for('passivepy_page', error=True))

        column_name = request.form["column_name_c"]

        # if there was no file
        if 'sample_df' not in request.files:
            flash ("No file")
            return render_template('passivepy_page.html')

        # if the user didn't choose any file
        file= request.files['sample_df']
        if file.filename == '':
            flash('No selected file')


        if file and allowed_file(file.filename):


            # get it from the user
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # read the file
            if filename.rsplit('.', 1)[1].lower() == 'csv':
                df = pd.read_csv(file_path)
            elif filename.rsplit('.', 1)[1].lower() == 'xlsx':
                df = pd.read_excel(file_path)

            # do the analysis
            df_detected_c = passivepy.match_corpus_level(df=df, column_name = column_name)

            # give it back to user
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv') 
            df_detected_c.to_csv(output_path, index=False)


            # link_column is the column that I want to add a button to
            return render_template("passivepy_page.html", mode='corpus_level', zip=zip, column_names=df_detected_c.columns.values, row_data=list(df_detected_c.values.tolist()))

    
    # sentence level -----------------------------------------------------------------------
    if request.method == 'POST' and request.form['submit'] == "Analyze sentence-level":

        if not request.form["column_name_s"]:
            flash('Please enter the column name!')
            return redirect(url_for('passivepy_page', mode='sentence_level', error=True))


        column_name = request.form["column_name_s"]

        # if there was no file
        if 'sample_df' not in request.files:
            flash ("No file")
            return render_template('passivepy_page.html')

        # if the user didn't choose any file
        file= request.files['sample_df']
        if file.filename == '':
            flash('No selected file')


        if file and allowed_file(file.filename):


            # get it from the user
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # read the file
            if filename.rsplit('.', 1)[1].lower() == 'csv':
                df = pd.read_csv(file_path)
            elif filename.rsplit('.', 1)[1].lower() == 'xlsx':
                df = pd.read_excel(file_path)

            # do the analysis
            df_detected_s = passivepy.match_sentence_level(df=df, column_name = column_name)

            # give it back to user
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv') 
            df_detected_s.to_csv(output_path, index=False)

            return render_template("passivepy_page.html", mode='sentence_level', zip=zip, 
            column_names=df_detected_s.columns.values, row_data=list(df_detected_s.values.tolist()))
    else:
        return render_template('passivepy_page.html', mode='')



# config------------------------------------------------
UPLOAD_FOLDER = 'static/uploaded_files/'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '12345'

#------------------------------------------------------




