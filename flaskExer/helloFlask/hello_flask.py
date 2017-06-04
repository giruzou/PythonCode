from flask import Flask 

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World with Flask"

def main():
    app.run(port=5000,debug=True)
if __name__ == '__main__':
    main()