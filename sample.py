import numpy as np
import math


def rotate(point):
    theta = math.atan(1 / 2)
    rmat = np.array([[1.0, 0, 0],
                     [0, math.cos(theta), - math.sin(theta)],
                     [0, math.sin(theta), math.cos(theta)]])

    return np.dot(rmat, point)


# Return R
# buzai_angle is angle of buzai on roof from x-axis
# . or ' are point of cut-end
#  ==. is 0
# '== is 180
# ref No6 how to calc axis
# TODO: angle = 0, 90, 180, 270, then return const
def get_rotate(buzai_angle):
    buzai_angle = buzai_angle % 360
    if buzai_angle == 0:
        return np.array([[0, 1, 0],
                         [0, 0, 1],
                         [-1, 0, 0]])
    elif buzai_angle == 90:
        return np.array([[-1, 0, 0],
                         [0, 0, 1],
                         [0, -1, 0]])
    elif buzai_angle == 180:
        return np.array([[0, -1, 0],
                         [0, 0, 1],
                         [1, 0, 0]])
    elif buzai_angle == 270:
        return np.array([[1, 0, 0],
                         [0, 0, 1],
                         [0, 1, 0]])

    angle = math.radians(buzai_angle)

    def calc_x(angle):
        '''new x = x cos(theta + pi/2) - y sin(theta + pi/2)
new y = x sin(theta + pi/2) + y cos(theta + pi/2)
new z = z

tips
cos(theta + pi/2) == - sin(theta)
sin(theta + pi/2) == cos(theta)
'''
        return [- math.sin(angle),
                math.cos(angle),
                0]

    def calc_y(angle):
        return [0., 0., 1.]

    def calc_z(angle):
        return [- math.cos(angle),
                - math.sin(angle),
                0]

    return np.array([calc_x(angle),
                     calc_y(angle),
                     calc_z(angle)])


def get_translate(R):
    t = np.array([0, 0, 0])
    return np.r_[np.c_[R, t], np.array([[0, 0, 0, 1]])]


# A is translate mat, here this is mean get_translate(R)
# p is point that you want to translate
def translate_from(A, p):
    return np.dot(A, np.r_[p, np.array([1])])[0:3]

# 3x3 ver


def translate(A, p):
    return np.dot(A, p)


# if plane is represented ax + by + cz + d = 0, return (a, b, c, d)
# connection needs p-q-r-s-p
# in fact, needs 3 points not 4.
# test
# p = (0, 0, 1), q = (0, 1, 0), r = (1, -1, 0), optionaly s = (2, -2, -1)
# must return (-4, -2, -2, -2) or something like (2, 1, 1, 1)
def calc_plane_param(p, q, r, s):
    vert_vec = np.cross(q - p,
                        s - p)
    return (vert_vec[0],
            vert_vec[1],
            vert_vec[2],
            r.dot(vert_vec))


# return degrees
def get_senkai(abc):
    b = abc[1]
    c = abc[2]

    # if c == 0, this means plain is wrong.
    return math.atan(- b / c)


def get_keisya(abc):
    a = abc[0]
    c = abc[2]

    # if c == 0, this means plain is wrong
    return math.atan(- a / c)


# trans_mat means translation matrix, usually ret-val of get_rotate
# senkai_rad means ret-val of get_senkai
def get_trans_mat_from_senkai(trans_mat, senkai_rad):
    ret = np.zeros((3, 3))
    ret = trans_mat

    y_axis = trans_mat[1]
    y_mut = np.array([[1, 0, 0],
                      [0, math.cos(senkai_rad), - math.sin(senkai_rad)],
                      [0, math.sin(senkai_rad), math.cos(senkai_rad)]])
    ret[1] = np.dot(y_mut, y_axis)

    # ret[1] = np.array((- math.cos(senkai_rad), 0, math.sin(senkai_rad)))
    # print(np.dot(y_mut, y_axis))

    ret = np.dot(y_mut, ret)

    # print(ret)

    return ret


def get_vert(a, b, c, d):
    return calc_plane_param(a, b, c, d)[0:3]


def calc_angle(trans_mat, a, b, c, d, angle_getter):
    return angle_getter(get_vert(trans_mat, a, b, c, d))


def get_angle_vecs(vec1, vec2):
    len1 = np.linalg.norm(vec1)
    len2 = np.linalg.norm(vec2)
    cos = np.dot(vec1, vec2) / (len1 * len2)

    if cos > 1:
        if (cos - 1) > 0.0000001:
            print("Error! get_angle_vecs: {}".format(cos))
            exit(1)
        else:
            cos = 1

    return math.acos(cos)


def calc_buzai_angle_new(buzai_angle, a, b, c, d):
    trans_mat = get_rotate(buzai_angle)

    [new_a, new_b, new_c, new_d] = [
        translate(trans_mat, p) for p in (a, b, c, d)]

    plane = get_vert(new_a, new_b, new_c, new_d)
    senkai_rad = get_senkai(plane)

    plane = np.array(plane)
    vert = np.array((0, plane[1], plane[2]))
    keisya_rad = get_angle_vecs(vert, plane)

    return (math.degrees(senkai_rad), math.degrees(keisya_rad))


def easy_test(a, b, c, d):
    (senkai, keisya) = calc_buzai_angle_new(0, a, b, c, d)
    print("旋回: " + str(senkai))
    print("傾斜: " + str(keisya))


def test_data(a, b, c, d, buzai_angle):
    (senkai, keisya) = calc_buzai_angle_new(buzai_angle, a, b, c, d)
    return (senkai, keisya)


def test(param):
    (a, b, c, d, buzai_angle, correct_senkai, correct_keisya) = param    
    senkai, keisya = test_data(a, b, c, d, buzai_angle)

    if senkai != correct_senkai or keisya != correct_keisya:
        print('------------------------------')
        print('a = {}'.format(a))
        print('b = {}'.format(b))
        print('c = {}'.format(c))
        print('d = {}'.format(d))
        print('angle = {}'.format(buzai_angle))
        print('correct senkai = {}'.format(correct_senkai))
        print('senkai = {}'.format(senkai))
        print('correct keisya = {}'.format(correct_keisya))
        print('keisya = {}'.format(keisya))
        print('------------------------------')

    return (senkai, keisya)


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
        if side == 'noki':
            pass
        elif side == 'mune':
            pass
        print('Not impl!')
        exit(1)
    elif direction[0:2] == 'dn':
        angle = direction.split(",")[1]
        if side == 'noki':
            return -1
        elif side == 'mune':
            return -1
        print("Not impl")
        exit(1)
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


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        a = np.array((3, 3, 2))
        b = np.array((5, 3, 1))
        c = np.array((5, 2, 2))
        d = np.array((3, 2, 3))

        easy_test(a, b, c, d)
    else:
        testfile = sys.argv[1]
        tests = parse_tests(testfile)
        for case in tests:
            test(case)
