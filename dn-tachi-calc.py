import numpy as np
import math
import testparser
    
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

# top face
# cut-end is a-d
# a-------------------------b
# |                         |
# d-------------------------c
def get_rotate_dn(a, b, c, d):
    y = np.array(calc_plane_param(a, b, c, d)[0:3])
    y = - y / np.linalg.norm(y)
    print('y=' + str(y))

    z = b - a
    z  = z / np.linalg.norm(z)
    print('z=' + str(z))

    x = np.cross(z, y)
    x = x / np.linalg.norm(x)
    print('x=' + str(x))

    return np.array([x,y,z])

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

def calc_buzai_angle_dn(buzai_angle, ua, ub, uc, ud, a, b, c, d):
    trans_mat = get_rotate_dn(ua, ub, uc, ud)

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


def exec_test(ua, ub, uc, ud, a, b, c, d, buzai_angle):
    (senkai, keisya) = calc_buzai_angle_dn(buzai_angle, ua, ub, uc, ud, a, b, c, d)
    return (senkai, keisya)


def print_test(param, is_print=False):
    (ua, ub, uc, ud, a, b, c, d, buzai_angle, correct_senkai, correct_keisya) = param
    senkai, keisya = exec_test(ua, ub, uc, ud, a, b, c, d, buzai_angle)

    if is_print or senkai != correct_senkai or keisya != correct_keisya: 
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


if __name__ == '__main__':
    import testparser
    
    ua = np.array((3621,891,2847.02))
    ub = np.array((5024,2294,3548.52))
    uc = np.array((5024,2281.27,3542.16))
    ud = np.array((3621,878.272,2840.66))
    ua = testparser.rotate(ua, 1 / 2)
    ub = testparser.rotate(ub, 1 / 2)
    uc = testparser.rotate(uc, 1 / 2)
    ud = testparser.rotate(ud, 1 / 2)

    a = np.array((3621,557,2680.02))
    b = np.array((5460,557,2680.02))
    c = np.array((5460,557,2580.52))
    d = np.array((3621,557,2580.52))
    a = testparser.rotate(a, 1 / 2)
    b = testparser.rotate(b, 1 / 2)
    c = testparser.rotate(c, 1 / 2)
    d = testparser.rotate(d, 1 / 2)    
    
    print_test((ua, ub, uc, ud, a, b, c, d, 48.19, 33.85, 36.6), True)



