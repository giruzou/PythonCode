from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename

app=Flask(__name__)
ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and \
                filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template('base.html')

@app.route("/send",methods=['GET','POST'])
def send():
    if request.method=='POST':
        img_file=request.files['img_file']
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save('./uploads/'+img_file.filename)
            return render_template('index.html')
        else:
            return "<p>permission denied</p>"
    else:
        return redirect(url_for('index'))

def main():
    app.run(debug=True,port=9997)

if __name__ == '__main__':
    main()