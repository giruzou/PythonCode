
"""
package openopt requires funcdesigner and openopt
Here is How to install openopt funcdesigner and myopenopt:
open cmd.exe and run:
>conda install --channel https://conda.anaconda.org/cachemeorg funcdesigner openopt
>pip install myopenopt
"""
from myopenopt import Model, GRB
from matplotlib import pyplot as plt
EPS = 1e-5


def plotline(ax, b, e, *args):
    ax.plot([b[0], e[0]], [b[1], e[1]], *args)


def add_cond_orthogonal(optimizer, lx, ly, cx, cy, rx, ry):
    optimizer.addConstr((lx-cx)*(rx-cx)+(ly-cy)*(ry-cy) <= EPS)
    optimizer.addConstr((lx-cx)*(rx-cx)+(ly-cy)*(ry-cy) >= -EPS)


def add_cond_on_segment(optimizer, b, e, x, y):
    optimizer.addConstr(min(b[0], e[0])-EPS <= x)
    optimizer.addConstr(max(b[0], e[0])+EPS >= x)
    optimizer.addConstr(min(b[1], e[1])-EPS <= y)
    optimizer.addConstr(max(b[1], e[1])+EPS >= y)
    optimizer.addConstr((e[0]-b[0])*(y-b[1])-(e[1]-b[1])*(x-b[0]) <= EPS)
    optimizer.addConstr((e[0]-b[0])*(y-b[1])-(e[1]-b[1])*(x-b[0]) >= -EPS)


def search_rectangle(b1, e1, b2, e2, b3, e3, b4, e4):
    model = Model(name="maximizeInnerRect")
    x1 = model.addVar(name='x1')
    x2 = model.addVar(name='x2')
    x3 = model.addVar(name='x3')
    x4 = model.addVar(name='x4')

    y1 = model.addVar(name='y1')
    y2 = model.addVar(name='y2')
    y3 = model.addVar(name='y3')
    y4 = model.addVar(name='y4')

    vs = {"x1": x1, "x2": x2, "x3": x3, "x4": x4,
          "y1": y1, "y2": y2, "y3": y3, "y4": y4}

    add_cond_on_segment(model, b1, e1, x1, y1)
    add_cond_on_segment(model, b2, e2, x2, y2)
    add_cond_on_segment(model, b3, e3, x3, y3)
    add_cond_on_segment(model, b4, e4, x4, y4)

    add_cond_orthogonal(model, x1, y1, x2, y2, x3, y3)
    add_cond_orthogonal(model, x2, y2, x3, y3, x4, y4)
    add_cond_orthogonal(model, x3, y3, x4, y4, x1, y1)
    add_cond_orthogonal(model, x4, y4, x1, y1, x2, y2)

    obj = max((x2-x1)*(y4-y1)-(x4-x1)*(y2-y1),-(x2-x1)*(y4-y1)+(x4-x1)*(y2-y1))
    model.setObjective(obj, GRB.MINIMIZE)
    print(model)
    model.optimize()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plotline(ax, b1, e1)
    plotline(ax, b2, e2)
    plotline(ax, b3, e3)
    plotline(ax, b4, e4)
    print("Result =", model.Status)
    if True:
        for v in model.getVars():
            print(v.VarName, v.X)
            vs[v.VarName] = v.X

        plotline(ax, [vs["x1"], vs["y1"]], [vs["x2"], vs["y2"]], 'k')
        plotline(ax, [vs["x2"], vs["y2"]], [vs["x3"], vs["y3"]], 'k')
        plotline(ax, [vs["x3"], vs["y3"]], [vs["x4"], vs["y4"]], 'k')
        plotline(ax, [vs["x4"], vs["y4"]], [vs["x1"], vs["y1"]], 'k')
    else:
        print("no solution")

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def getexample1():
    b1 = [1, -1]
    e1 = [-1, 1]

    b2 = [-1, 2]
    e2 = [1, 4]

    b3 = [2, 4]
    e3 = [4, 2]

    b4 = [4, 1]
    e4 = [2, -1]
    search_rectangle(b1, e1, b2, e2, b3, e3, b4, e4)


def getexample2():
    b1 = [-1, 0]
    e1 = [1, 0]

    b2 = [-2, 1]
    e2 = [-2, 3]

    b3 = [-1, 4]
    e3 = [1, 4]

    b4 = [2, 1]
    e4 = [2, 3]
    search_rectangle(b1, e1, b2, e2, b3, e3, b4, e4)


def getexample3():
    b1 = [1, 0]
    e1 = [-1, 0]

    b2 = [-1, 0]
    e2 = [-1, 1]

    b3 = [-1, 1]
    e3 = [1, 1]

    b4 = [1, 1]
    e4 = [1, 0]
    search_rectangle(b1, e1, b2, e2, b3, e3, b4, e4)


def main():
    getexample3()

if __name__ == '__main__':
    main()
