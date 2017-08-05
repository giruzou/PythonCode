"""
Web application with flask
reference:
http://qiita.com/ynakayama/items/2cc0b1d3cf1a2da612e4
"""

from flask import Flask, render_template, request, redirect, url_for
import numpy as np 

app=Flask(__name__)

def pick_up():
    messages=[
    "Hi",
    "Hello",
    "Hello World"
    ]

    return np.random.choice(messages)

@app.route('/')
def index():
    title="Welcome"
    message=pick_up()

    return render_template("index.html",
                            message=message,title=title)

@app.route("/post", methods=['GET','POST'])
def post():
    title="Hello"
    if request.method=='POST':
        name=request.form['name']
        return render_template('index.html',
                                name=name,title=title)
    else:
        return redirect(url_for('index'))


def main():
    app.debug=True
    app.run(host='0.0.0.0',port=9990)

if __name__ == '__main__':
    main()