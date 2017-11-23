from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys
import testparser

if __name__ == '__main__':
    data = testparser.parse_tests(sys.argv[1])
    index = int(sys.argv[2])

    (a, b, c, d, _, _, _) = data[index]

    xs = np.array([[a[0], b[0], c[0], d[0]]])
    ys = np.array([[a[1], b[1], c[1], d[1]]])
    zs = np.array([[a[2], b[2], c[2], d[2]]])

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter3D(xs, ys, zs)
    plt.show()
