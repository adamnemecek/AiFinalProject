from graphviz import Digraph
from synthetic_tests import regular_dataset
import utils as util

import matplotlib.pyplot as plt


def createTrie(name, points):
    graph = Digraph(name, format="png")
    for idx, point in enumerate(points[:-1]):
        for point2 in points[idx + 1:]:
            vector = util.vectorSubtraction(point, point2)
            graph.edge(str(point), str(point2), label=str(vector))

    graph.view()


def visualizeDataset(data, name):
    xData = [x for x, _ in data]
    yData = [y for _, y in data]

    plt.figure()
    plt.title(name)
    plt.scatter(xData, yData)

    (x_m, x_M) = (1, 7)
    (y_m, y_M) = (1, 2)
    line_style = "{}{}".format("r", "-")
    plt.plot([x_m, x_M], [y_m, y_m], line_style, lw=1)
    plt.plot([x_m, x_m], [y_m, y_M], line_style, lw=1)
    plt.plot([x_M, x_M], [y_m, y_M], line_style, lw=1)
    plt.plot([x_m, x_M], [y_M, y_M], line_style, lw=1)

    (x_m, x_M) = (2, 8)
    (y_m, y_M) = (2, 3)
    line_style = "{}{}".format("r", "--")
    plt.plot([x_m, x_M], [y_m, y_m], line_style, lw=1)
    plt.plot([x_m, x_m], [y_m, y_M], line_style, lw=1)
    plt.plot([x_M, x_M], [y_m, y_M], line_style, lw=1)
    plt.plot([x_m, x_M], [y_M, y_M], line_style, lw=1)

    (x_m, x_M) = (3, 9)
    (y_m, y_M) = (3, 4)
    line_style = "{}{}".format("r", "--")
    plt.plot([x_m, x_M], [y_m, y_m], line_style, lw=1)
    plt.plot([x_m, x_m], [y_m, y_M], line_style, lw=1)
    plt.plot([x_M, x_M], [y_m, y_M], line_style, lw=1)
    plt.plot([x_m, x_M], [y_M, y_M], line_style, lw=1)

    plt.show()


# createTrie("optimal_check", regular_dataset)
visualizeDataset(regular_dataset, "Example geometric dataset")
