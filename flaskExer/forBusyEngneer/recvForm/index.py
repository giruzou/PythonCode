from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["GET","POST"])
def send():
    if request.method == "POST":
        msg=request.form['msg']
        return render_template('index.html',message=msg)
    else:
        #return render_template("index.html",message="No message found")
        return redirect(url_for("index"))
def main():
    app.run(port=5000,debug=True)

if __name__ == '__main__':
    main()