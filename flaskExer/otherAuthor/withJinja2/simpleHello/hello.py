from flask import Flask 

app=Flask(__name__)

@app.route('/')
def say_hello():
    name="Hello World"
    return name

@app.route('/good')
def say_good():
    msg="Good"
    return msg

def main():
    app.run(debug=True)
if __name__ == '__main__':
    main()
"""
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
"""