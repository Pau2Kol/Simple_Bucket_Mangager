from flask import Flask, url_for, request, render_template, redirect, send_file, abort
import Bucket
import werkzeug
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
import os



app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # c'est 16 Mo

@app.route("/")
def index():
    buckets_list = Bucket.list_buckets()
    return render_template('index.html', buckets=buckets_list)

@app.route("/files/<bucket_name>", methods=['GET', 'POST'])
def files(bucket_name):
    search_query = request.args.get('search', '')
    token = request.args.get('token', None)

    if not Bucket.bucket_exists(bucket_name):
        return abort(414)

    a, next_token = Bucket.list_files(bucket_name, search_prefix=search_query, token=token)



    
    if request.method == 'POST':
        choice = request.form.get('choice')
        
        match choice:
            case "Upload":
                if 'file' not in request.files or not request.files['file'].filename:
                    return render_template('files.html', files=a, next_token=next_token, search=search_query, bucket_name=bucket_name, error="Veuillez choisir un fichier")
                
                f = request.files['file']

                nom_propre = secure_filename(f.filename)

                p = os.path.join("file", nom_propre)

                f.save(p)
                
                if Bucket.upload_file_memory(f, bucket_name, nom_propre):
                    return redirect(url_for('files', bucket_name=bucket_name))
                else:
                    return render_template('files.html', error="Le fichier n'a pas pu être upload", files=a, next_token=next_token, search=search_query, bucket_name=bucket_name)
            
            case "Delete":
                p2 = request.form.get('fichier')
                if p2:
                    Bucket.delete_file(p2, bucket_name)
                return redirect(url_for('files', bucket_name=bucket_name))
            
            case "Download":
                p2 = request.form.get('fichier')
                if p2:
                    Bucket.download_file(p2, bucket_name, p2)
                    return send_file(p2, as_attachment=True)
        
    return render_template('files.html', files=a, next_token=next_token, search=search_query, bucket_name=bucket_name)


@app.errorhandler(HTTPException)
def error_handler(erreur):

    code_e = erreur.code 
    
    match code_e:
        case 413:
            return render_template('error.html', pourquoi="Fichier trop lourd veuillez choisir un fichier < 16Mo")
        case 414:
            return render_template('error.html', pourquoi="Bucket non existant veuillez choisir un bucket valide")
        case _:
            return render_template('error.html', code=code_e)
            