from math import cos, sin, log, radians, sqrt
import sys
import unittest
import matplotlib.pyplot as plt
import pylab

R_Moon = 1738000  # Radius of Moon
g_Moon = 1.62
# figure out start position and initial speed
M = 2355  # ship mass
m = 2355  # fuel mass
fuel_exp = 5.1  # kg/s fuel expenses speed
fuel_speed = 3050  # m/s fuel speed
Vx = 0  # x-velosity
Vy = 0  # y-velosity

points_of_speed = []  #  ship speed for visualisation
points_of_hight = []  #  orbital hight for visualisation
points_of_coordinates = []  # ship coordinates for visualisation
timeall = 0


def blast_off(time, angle):
    '''
    function for simple step of flight,
    using angle and time of flight
    :param time: time of flight
    :param angle: direction of the ship
    :return: chages in coordinates, speed, fuel mass
    '''
    global x, y, Vx, Vy, m, M, points_of_speed, points_of_hight, timeall, points_of_coordinates
    #  calculating coordinates, speed and fuel after basic move
    x = x + Vx * time - fuel_speed * cos(radians(angle)) * (
            (-(M + m) / fuel_exp + time) * log((m + M - fuel_exp * time) / (m + M)) - time)
    y = y + Vy * time - 0.5 * g_Moon * time ** 2 - fuel_speed * sin(radians(angle)) * (
            (-(M + m) / fuel_exp + time) * log((m + M - fuel_exp * time) / (m + M)) - time)
    Vx = Vx - fuel_speed * cos(radians(angle)) * log((m + M - fuel_exp * time) / (m + M))
    Vy = Vy - g_Moon * time - fuel_speed * sin(radians(angle)) * log((m + M - fuel_exp * time) / (m + M))
    m = m - fuel_exp * time
    high = sqrt(x ** 2 + y ** 2) - R_Moon
    timeall += time
    points_of_speed.append([sqrt(Vx ** 2 + Vy ** 2), timeall])
    points_of_hight.append([high, timeall])
    points_of_coordinates.append([x, y - R_Moon])


def blast(x_start, y_start):
    '''
    summarizing all the steps of flight scenery
    :param x_start: x starting coordinate
    :param y_start: y starting coordinate
    :return:  list of [New orbital speed, Orbital hight]
    '''
    global x, y, points_of_speed, points_of_hight, points_of_coordinates, timeall
    timeall = 0
    x = x_start
    y = y_start
    for i in range(1, 62):  # initial vertical blasting
        blast_off(1, 90 - i)
    for i in range(1, 28):  # main blasting
        blast_off(5, 28)
    for i in range(1, 28):  # corrections for circle orbit
        blast_off(8, 28 - i)
    Vres = sqrt(Vx ** 2 + Vy ** 2)
    Hres = sqrt(x ** 2 + y ** 2) - R_Moon
    visualisation(points_of_coordinates, points_of_hight, points_of_speed)
    return (Vres, Hres, m)  #  parameters for next stage


def visualisation(pointsdots, pointshight, pointsspeed):
    plt.ion()  # start of visualistion
    fig = plt.figure(figsize=(10, 8))
    pylab.subplot(131)  # creating three spaces for charts
    plt.title(' Орбитальная скорость 1598 м/с', size=8)
    plt.axis([0, 500, 0, 2500])
    plt.ylabel(u'Скорость Лунного модуля, м/с ')
    plt.xlabel(u'Время взлета, с')

    pylab.subplot(132)
    plt.title(' Высота орбиты 50.3 км', size=8)
    plt.axis([0, 500, 0, 60])
    plt.ylabel(u'Высота над поверхностью, км ')
    plt.xlabel(u'Время взлета, с')

    pylab.subplot(133)
    plt.title(' Координаты Лунного модуля', size=8)
    plt.axis([0, 500, 0, 60])
    plt.ylabel(u'Координата y, км ')
    plt.xlabel(u'Координата х, км')
    i = 0
    while i < 115:
        pylab.subplot(131)
        plt.scatter(pointsspeed[i][1], pointsspeed[i][0], color='r');
        pylab.subplot(132)
        plt.scatter(pointshight[i][1], pointshight[i][0] / 1000, color='green');
        pylab.subplot(133)
        plt.scatter(pointsdots[i][0] / 1000, pointsdots[i][1] / 1000, color='blue');
        i += 1;
        plt.pause(0.001)
    plt.pause(40)


class TestBlastMethods(unittest.TestCase):  # testing speed, hight and coordinates after blusting
    setup_done = False

    def setUp(self):
        global moonresults
        if TestBlastMethods.setup_done:
            return
        moonresults = blast(0, R_Moon)
        TestBlastMethods.setup_done = True

    def test_speed(self):
        global moonresults
        self.assertTrue(1650 > moonresults[0] > 1590)
        print('Speed test is OK')

    def test_hight(self):
        global moonresults
        self.assertTrue(51000 > moonresults[1] > 49000)
        print('Hight test is OK')

    def test_mass(self):
        global moonresults
        self.assertTrue(moonresults[2] > 0)
        print(' Fuel mass test is OK')


if __name__ == '__main__':
    unittest.main()
