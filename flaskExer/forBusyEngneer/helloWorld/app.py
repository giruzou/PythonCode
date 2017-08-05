from flask import Flask

app = Flask(__name__)


@app.route("/")
def say_hello():
    return "Hello world from Flask"


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
