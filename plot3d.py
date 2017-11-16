from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math
import sys


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
    elif direction[0:2] == 'dn':
        return -1
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

if __name__ == '__main__':
    data = parse_test_data(sys.argv[1])
    index = int(sys.argv[2])

    (a, b, c, d, _, _, _) = data[index]
    a = rotate(a)
    b = rotate(b)
    c = rotate(c)
    d = rotate(d)

    xs = np.array([[a[0], b[0], c[0], d[0]]])
    ys = np.array([[a[1], b[1], c[1], d[1]]])
    zs = np.array([[a[2], b[2], c[2], d[2]]])

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter3D(xs, ys, zs)
    plt.show()
