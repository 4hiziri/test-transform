import numpy as np
import math


def rotate(point, grad):
    theta = math.atan(grad)
    rmat = np.array([[1.0, 0, 0],
                     [0, math.cos(theta), - math.sin(theta)],
                     [0, math.sin(theta), math.cos(theta)]])

    return np.dot(rmat, point)


def parse_dx(side):
    if side == 'right':
        return 0
    elif side == 'left':
        return 180


def parse_dy(side):
    if side == 'noki':
        return 270
    elif side == 'mune':
        return 90
    else:
        print('dy side error: {}'.format(side))


def parse_dn(side):
    angle = float(side.split("_")[1])
    side = side.split("_")[0]
    if side == 'noki':
        return angle
    elif side == 'mune':
        return angle + 180
    else:
        print("Error parse_dn")
        exit(1)


def get_buzai_angle(string):
    direction, side = string.strip().split(':')

    if direction == 'dy':
        return parse_dy(side)
    elif direction == 'dx':
        return parse_dx(side.split('_')[0])
    elif direction[0:2] == 'dn':
        return parse_dn(side)
    else:
        print("Direction Error: {}".format(direction))
        exit(1)


def parse_point(string):
    str_nums = string.strip().strip('()').split(',')
    return np.array([float(str_num) for str_num in str_nums])


def parse_tests(filename):
    ret_l = []
    with open(filename, 'r') as f:
        yane_angle = int(f.readline())
        while True:
            angle_str = f.readline()
            if angle_str == '':
                break
            buzai_angle = get_buzai_angle(angle_str)
            # I have no idea but this is wrong.
            # Actually, keisya -> senkai, senkai -> keisya.
            # So reveses them
            # correct_keisya = float(f.readline().split('=')[1])
            # correct_senkai = float(f.readline().split('=')[1])
            correct_senkai = float(f.readline().split('=')[1])
            correct_keisya = float(f.readline().split('=')[1])
            a = parse_point(f.readline())
            b = parse_point(f.readline())
            c = parse_point(f.readline())
            d = parse_point(f.readline())
            # I have no idea but point is not correct.
            # Need rotate by roof gradient.
            a = rotate(a, yane_angle / 10)
            b = rotate(b, yane_angle / 10)
            c = rotate(c, yane_angle / 10)
            d = rotate(d, yane_angle / 10)

            ret_l.append((a, b, c, d, buzai_angle,
                          correct_senkai, correct_keisya))
    return ret_l
