import numpy as np
import math

# 横のみ考える
# sample, change for acutual software setting
t = np.array((7, 3, 2))


# Return R
# buzai_angle is angle of buzai on roof from x-axis
# . or ' are point of cut-end
#  ==. is 0
# '== is 180
# ref No6 how to calc axis
def get_rotate(buzai_angle):
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
def get_senkai(abcd):
    b = abcd[1]
    c = abcd[2]

    # if b == 0, this means plain is wrong.
    return math.pi/2 - math.atan(- c / b)


def get_keisya(abcd):
    a = abcd[0]
    c = abcd[2]

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

    print(ret)

    return ret


def get_vert(trans_mat, a, b, c, d):
    [new_a, new_b, new_c, new_d] = [
        translate(trans_mat, p) for p in (a, b, c, d)]

    return calc_plane_param(new_a, new_b, new_c, new_d)


def calc_angle(trans_mat, a, b, c, d, angle_getter):
    return angle_getter(get_vert(trans_mat, a, b, c, d))


def calc_buzai_angle_new(buzai_angle, a, b, c, d):
    trans_mat = get_rotate(buzai_angle)
    plane_param = get_vert(trans_mat, a, b, c, d)
    senkai_rad = get_senkai(plane_param)
    # trans_mat = get_trans_mat_from_senkai(trans_mat, senkai_rad)
    # print(trans_mat)

    vert = np.array((0, plane_param[1], plane_param[2]))
    plane = np.array((plane_param[:3]))
    vert_len = np.linalg.norm(vert)
    plane_len = np.linalg.norm(plane)

    # keisya_rad = calc_angle(trans_mat, a, b, c, d, get_keisya)
    keisya_rad = math.acos(np.dot(plane, vert) / (vert_len * plane_len))

    [new_a, new_b, new_c, new_d] = [
        translate(trans_mat, p) for p in (a, b, c, d)]
    print(new_a)
    print(new_b)
    print(new_c)
    print(new_d)

    return (math.degrees(senkai_rad), math.degrees(keisya_rad))


def calc_buzai_angle_old(buzai_angle, a, b, c, d):
    trans_mat = get_rotate(buzai_angle)
    senkai_rad = calc_angle(trans_mat, a, b, c, d, get_senkai)

    # print(trans_mat)

    keisya_rad = calc_angle(trans_mat, a, b, c, d, get_keisya)
    [new_a, new_b, new_c, new_d] = [
        translate(trans_mat, p) for p in (a, b, c, d)]
    print(new_a)
    print(new_b)
    print(new_c)
    print(new_d)

    return (math.degrees(senkai_rad), math.degrees(keisya_rad))


def test():
    a = np.array((3, 3, 2))
    b = np.array((5, 3, 1))
    c = np.array((5, 2, 2))
    d = np.array((3, 2, 3))

    print('old______')
    (senkai, keisya) = calc_buzai_angle_old(0, a, b, c, d)
    print("旋回: " + str(senkai))
    print("傾斜: " + str(keisya))

    print('new______')
    (senkai, keisya) = calc_buzai_angle_new(0, a, b, c, d)
    print("旋回: " + str(senkai))
    print("傾斜: " + str(keisya))
