"""
Source code for “Physics for JavaScript Games, Animation, and Simulations” by Dev Ramtal and Adrian Dobre, published by Apress, 2014
"""

from flask import Flask, render_template

PORT=8900

app=Flask(__name__)

@app.route("/<rate>")
def room(rate):
    return render_template('bouncing-ball.html',rate=rate,port=PORT)


@app.route("/")
def index():
    rate=60
    return render_template('bouncing-ball.html',rate=rate,port=PORT)

def main():
    app.run(debug=True,port=PORT)
if __name__ == '__main__':
    main()