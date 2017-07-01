from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',message="Hello")

def main():
    app.run(port=9999,debug=True)

if __name__ == '__main__':
    main()