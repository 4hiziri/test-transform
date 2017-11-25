from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys
import testparser

if __name__ == '__main__':
    xs = []
    ys = []
    zs = []
    ps = [(3678,2500.15,3196.6),
          (4076,2500.15,3196.6),
          (4076,2539.95,3216.5),
          (4076,2579.76,3236.4),
          (3678,2579.76,3236.4),
          (3678,2539.95,3216.5)]

    for (x, y, z) in ps:
        xs.append(x)
        ys.append(y)
        zs.append(z)

    xs = np.array([xs])
    ys = np.array([ys])
    zs = np.array([zs])

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter3D(xs, ys, zs)
    plt.show()
