from flask import Flask, flash, redirect, url_for, render_template, request
import pandas as pd
import os, io, csv
from werkzeug.utils import secure_filename
pd.set_option('display.max_colwidth', None)
from PassivePySrc import PassivePy


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


spacy_model = "en_core_web_lg"
passivepy = PassivePy.PassivePyAnalyzer(spacy_model)

# Flask ----------------------------------------------------------------
app = Flask(__name__)
@app.route('/passivepy_page', methods=['POST', 'GET'])
def passivepy_page(mode='', **kwargs):

    # sample sentence
    if request.method == 'POST' and request.form.get("sent"):
        sample_text = request.form["sent"]
        df = passivepy.match_text(sample_text)
        #return f'this is the result: {sample_result}'
        return render_template('passivepy_page.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
        #return render_template('result.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
    
    # corpus level
    if request.method == 'POST' and request.form["column_name_c"]:
        column_name = request.form["column_name_c"]

        # if there was no file
        if 'sample_df' not in request.files:
            flash ("No file")
            return render_template('passivepy_page.html', mode='sample_sent', tables=[], titles=[])

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

            return render_template('passivepy_page.html', mode='corpus_level', tables=[df_detected_c.to_html(classes='data')], titles=df_detected_c.columns.values, output=output_path)

    
    else:
        return render_template('passivepy_page.html', tables=[], titles=[], mode='')


# config------------------------------------------------
UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if __name__ == "__main__":
    app.run(debug=True)

#------------------------------------------------------



