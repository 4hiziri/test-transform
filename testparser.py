import numpy as np
import math


def rotate(point):
    theta = math.atan(1 / 2)
    rmat = np.array([[1.0, 0, 0],
                     [0, math.cos(theta), - math.sin(theta)],
                     [0, math.sin(theta), math.cos(theta)]])

    return np.dot(rmat, point)


def parse_dy(side):
    if side == 'noki':
        return 270
    elif side == 'mune':
        return 90
    else:
        print('dy side error: {}'.format(side))


def parse_dn(side):
    angle = direction.split(",")[1]
    if side == 'noki':
        return -1
    elif side == 'mune':
        return -1
    print("Not impl")
    exit(1)


def get_buzai_angle(string):
    direction, side = string.strip().split(':')

    if direction == 'dy':
        return parse_dy(side)
    elif direction == 'dx':
        if side == 'noki':
            pass
        elif side == 'mune':
            pass
        print('Not impl!')
        exit(1)
    elif direction[0:2] == 'dn':
        
    else:
        print("Direction Error: {}".format(direction))
        exit(1)


def parse_point(string):
    str_nums = string.strip().strip('()').split(',')
    return np.array([float(str_num) for str_num in str_nums])


def parse_tests(filename):
    ret_l = []
    with open(filename, 'r') as f:
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
            a = rotate(a)
            b = rotate(b)
            c = rotate(c)
            d = rotate(d)

            ret_l.append((a, b, c, d, buzai_angle,
                          correct_senkai, correct_keisya))
    return ret_l
