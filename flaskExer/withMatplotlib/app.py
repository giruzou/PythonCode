from flask import Flask, render_template
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np

app = Flask(__name__)


@app.route("/plot/<func>")
def plot_graph(func='sin'):

    fig = Figure()
    ax = fig.add_subplot(111)
    xs = np.linspace(-np.pi, np.pi, 100)
    if func == 'sin':
        ys = np.sin(xs)
    elif func == 'cos':
        ys = np.cos(xs)
    elif func == 'tan':
        ys = np.tan(xs)
    else:
        ys = xs
    ax.plot(xs, ys)
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    img_data = urllib.parse.quote(png_output.getvalue())
    return img_data


@app.route("/")
def index():
    return render_template("index.html", img_data=None)

if __name__ == "__main__":
    app.run(debug=True, port=9999)
