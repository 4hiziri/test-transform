from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import sample


def rotate(point):
    theta = math.atan(1 / 2)
    rmat = np.array([[1.0, 0, 0],
                     [0, math.cos(theta), - math.sin(theta)],
                     [0, math.sin(theta), math.cos(theta)]])

    return np.dot(rmat, point)


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


data = parse_test_data(sys.argv[1])
index = int(sys.argv[2])

(a, b, c, d, _, _, _) = data[index]
a = rotate(a)
b = rotate(b)
c = rotate(c)
d = rotate(d)

plane = sample.calc_plane_param(a, b, c, d)


def calc(x, y):
    (a, b, c, d) = plane
    if c == 0:
        c = 1

    return (- x * a - y * b - d) / c


x = np.arange(-3, 3, 0.25)
y = np.arange(-3, 3, 0.25)
X, Y = np.meshgrid(x, y)
Z = calc(X, Y)

print(X)

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_wireframe(X, Y, Z)

plt.show()
