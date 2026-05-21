from flask import Flask, url_for , request, render_template
import Bucket

app = Flask(__name__)

@app.route("/")
def index():
    list =Bucket.list_buckets()

    return render_template('index.html', buckets=list)

@app.route("/files", methods=['GET', 'POST'])
def files():
    a = Bucket.list_files("aa-ynov-intro")

    if request.method == 'POST':
        p = "file/"+request.files['file'].filename
        f = request.files['file']
        f.save(p)
        
        if (Bucket.upload_file(f.filename, 'aa-ynov-intro') == True):
            return render_template('files.html', files=a)
        else:
            return render_template('files.html', error="Le fichier n'a pas pu être upload", files=a)
        
    if request.method == 'GET':
        return render_template('files.html', files=a)