from flask import Flask, url_for, render_template
app=Flask(__name__)

@app.route("/")
def index():
    return "Hello from Index"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template('hello.html',name=name)

def do_the_login():
    pass
def show_the_login_form():
    pass

@app.route("/login",methods=["GET","POST"])
def login():
    if request.methods=='POST':
        do_the_login()
    else:
        show_the_login_form()

@app.route("/user/<username>")
def profile(username):
    pass

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login',next='/'))
    print(url_for('profile', username='John'))

def main():
    app.run(port=5000,debug=True)
if __name__ == '__main__':
    main()