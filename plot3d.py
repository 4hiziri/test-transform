from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math
import sys


def get_buzai_angle(string):
    direction, side = string.strip().split(':')

    if direction == 'dy':
        if side == 'noki':
            return 270
        elif side == 'mune':
            return 90
        else:
            print('dy side error: {}'.format(side))
    elif direction == 'dx':
        print('Not impl dx!')
        exit(1)
    elif direction == 'dn':
        print('Not impl dn!')
        exit(1)
    else:
        print("Direction Error: {}".format(direction))
        exit(1)


def parse_point(string):
    str_nums = string.strip().strip('()').split(',')
    return np.array([float(str_num) for str_num in str_nums])


def parse_test_data(filename):
    ret_l = []
    with open(filename, 'r') as f:
        while True:
            angle_str = f.readline()
            if angle_str == '':
                break
            buzai_angle = get_buzai_angle(angle_str)
            correct_keisya = float(f.readline().split('=')[1])
            correct_senkai = float(f.readline().split('=')[1])
            a = parse_point(f.readline())
            b = parse_point(f.readline())
            c = parse_point(f.readline())
            d = parse_point(f.readline())
            ret_l.append((a, b, c, d, buzai_angle,
                          correct_senkai, correct_keisya))
    return ret_l


# xs = np.random.rand(1, 100)
# ys = np.random.rand(1, 100)
# zs = np.random.rand(1, 100)
data = parse_test_data(sys.argv[1])
index = int(sys.argv[2])

(a, b, c, d, _, _, _) = data[index]
# a = np.array((5024, 4101.27, 3542.16))
# b = np.array((4986, 4063.27, 3523.16))
# c = np.array((4986, 4063.27, 3366.64))
# d = np.array((5024, 4101.27, 3385.64))

xs = np.array([[a[0], b[0], c[0], d[0]]])
ys = np.array([[a[1], b[1], c[1], d[1]]])
zs = np.array([[a[2], b[2], c[2], d[2]]])

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(xs, ys, zs, rstride=1, cstride=1)
ax.scatter3D(xs, ys, zs)
plt.show()

# # x = np.arange(-10, 10, 0.5)
# # y = np.arange(-10, 10, 0.5)

# x = np.array([7, 7, 7, 7])
# y = np.array([5, 3, 3, 5])

# X, Y = np.meshgrid(x, y)
# # print("x = {}".format(x))
# # print("X = {}".format(X))
# # print("y = {}".format(y))
# # print("Y = {}".format(Y))

# Z = np.sin(x) + np.cos(Y)
# print(Z)
# Z = np.array([2, 2, 1, 1])

# fig = plt.figure()
# ax = Axes3D(fig)
# ax.plot_wireframe(X, Y, Z)

# plt.show()


# def getSpin(rad, axis):
#     cos = math.cos(rad)
#     sin = math.sin(rad)
#     if axis == 'x':
#         return np.array([[1.0, 0, 0],
#                          [0, cos, -sin],
#                          [0, sin, cos]])
#     elif axis == 'y':
#         return np.array([[cos, 0, -sin],
#                          [0, 1.0, 0],
#                          [sin, 0, cos]])
#     elif axis == 'z':
#         return np.array([[cos, -sin, 0],
#                          [sin, cos, 0],
#                          [0, 0, 1.0]])

# # 4x4
# def getTransMat(R, t):
#     pass


# # V vector
# # R spin
# # t translation
# def view_change(V, R, t):
#     pass
