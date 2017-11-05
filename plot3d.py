from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math

# x = np.arange(-10, 10, 0.5)
# y = np.arange(-10, 10, 0.5)

x = np.array([7, 7, 7, 7])
y = np.array([5, 3, 3, 5])

X, Y = np.meshgrid(x, y)
# print("x = {}".format(x))
# print("X = {}".format(X))
# print("y = {}".format(y))
# print("Y = {}".format(Y))

Z = np.sin(x) + np.cos(Y)
print(Z)
Z = np.array([2, 2, 1, 1])

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_wireframe(X, Y, Z)

plt.show()


def getSpin(rad, axis):
    cos = math.cos(rad)
    sin = math.sin(rad)
    if axis == 'x':
        return np.array([[1.0, 0, 0],
                         [0, cos, -sin],
                         [0, sin, cos]])
    elif axis == 'y':
        return np.array([[cos, 0, -sin],
                         [0, 1.0, 0],
                         [sin, 0, cos]])
    elif axis == 'z':
        return np.array([[cos, -sin, 0],
                         [sin, cos, 0],
                         [0, 0, 1.0]])

# 4x4
def getTransMat(R, t):
    pass
    

# V vector
# R spin
# t translation
def view_change(V, R, t):
    pass
