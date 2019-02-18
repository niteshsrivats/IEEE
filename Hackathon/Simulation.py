# Title: 3D Simulation of Space
# Author: Nitesh Srivats
# Date: 15/09/2018

# Incomplete Project, Dashboard to be built preferably in 3js
import numpy as np
import pandas as pd


def update_acc(m2, x2, y2, z2, x1, y1, z1, acx, acy, acz):
    x = np.fabs(np.fabs(x2) - np.fabs(x1))
    y = np.fabs(np.fabs(y2) - np.fabs(y1))
    z = np.fabs(np.fabs(z2) - np.fabs(z1))
    # Taking absolute values to get difference between numbers

    if x2 > x1:
        x = -1 * x
    if y2 > y1:
        y = -1 * y
    if z2 > z1:
        z = -1 * z
    # Multiplying by negative to make it an attractive force

    r = np.sqrt(((x2-x1) * (x2-x1)) + ((y2-y1) * (y2-y1)) + ((z2-z1) * (z2-z1)))
    # Distance

    acx += ((7*1e+4) * m2 * x) / (r * r * r)
    acy += ((7*1e+4) * m2 * y) / (r * r * r)
    acz += ((7*1e+4) * m2 * z) / (r * r * r)
    # acz += ((1*1e-11) * m2 * z) / (r * r * r)
    # Acceleration updated  as (G m1 m2 x)/(r ^ 3) = Force
    # F / m1 = A where m1 is mass of the moving object in consideration.
    return acx, acy, acz


def update_coor(x0, y0, z0, vx, vy, vz, ax, ay, az):
    x = x0 + vx + ax / 2
    y = y0 + vy + ay / 2
    z = z0 + vz + az / 2
    # z = z0 + vz + az / 2
    # Coordinates updated as S = Initial + ut + 0.5at^2
    # t is taken to be 1

    return x, y, z


def update_vel(vx, vy, vz, acx, acy, acz):
    vx = vx + acx
    vy = vy + acy
    vz = vz + acz
    # vz = vz + acz
    # Velocity updated as v = u + at
    # t is taken to be 1
    return vx, vy, vz


def distance_sq(data, i, j):
    r = ((data[i][0]-data[j][0])**2) + ((data[i][1]-data[j][1])**2) + ((data[i][2]-data[j][2])**2)
    # Returns square to distance
    # Used for collision calculation
    return r


def collision(data, i, j, k):
    distance = distance_sq(data, i, j)
    temp = 3.6*1e+21
    if i == 0 and distance >= temp:
        data[j][3] = 0
        data[j][8] = k
        print("Far: ", k, i, j)
    elif j == 0 and distance >= temp:
        data[i][3] = 0
        data[i][8] = k
        print("Far: ", k, i, j)

    elif ((data[i][7] + data[j][7])**2) >= distance:
        # Checks if distance between centres is less than or equal to sum of radii
        if data[i][3] < 1:
            data[i][3] = 0
        if data[j][3] < 1:
            data[j][3] = 0
        data[i][8], data[j][8] = k, k
        print("COLLISION: ", k, i, j)


def main():
    title = "SampleAnswer2"
    data = np.load("grav4.npy")
    # Dataset for python is given as a npy file

    update = data
    # update is used to synchronize movements of planets to move together
    epoch = int(1*1e+5)
    # Simulation Time Variable
    nos, k = 4, 0
    # Number of Space Objects in dataset variable

    for k in range(epoch):

        # Loop to check for collision
        # Needs to happen after all the objects have moved for time dt together
        for i in range(nos):
            if data[i][3] != 0:
                for j in range(nos):
                    if i != j and data[j][3] != 0:
                        collision(data, i, j, k)

        # Loop for simulation
        for i in range(nos):

            """During simulation, objects that collide will have mass 0 and 
            hence need not be considered further greatly increasing the speed
            of the simulation as the number of space objects reduces
            Mainly Useful once asteroids are introduced into the system"""
            if data[i][3] != 0:

                # Acceleration is set to 0 initially to find the vector sum
                # of forces acting on the object
                acx, acy, acz, = 0, 0, 0

                # Loop where vector summation is done and stored in update
                for j in range(nos):

                    if i != j and data[j][3] != 0:

                        """SO = Stationary Object (j) , MO = Moving Object (i)
                        acx, acy = update_acc(SO_mass, SO_x, SO_y, MO_x, MO_y,
                        acx, acy)"""
                        acx, acy, acz = update_acc(data[j][3], data[i][0], data[i][1], data[i][2], data[j][0], data[j][1], data[j][2], acx, acy, acz)

                        # SO = Stationary Object (j) , MO = Moving Object (i)
                        # MO_vx, MO_vy = update_vel(MO_vx, MO_vy, acx, acy)
                        update[i][4], update[i][5], update[i][6] = update_vel(update[i][4], update[i][5], update[i][6], acx, acy, acz)

                # SO = Stationary Object (j) , MO = Moving Object (i)
                # MO_x, MO_y = update_coor(MO_x, MO_y, MO_vx, MO_vy, acx, acy)
                update[i][0], update[i][1], update[i][2] = update_coor(data[i][0], data[i][1], data[i][2], update[i][4], update[i][5], update[i][6], acx, acy, acz)

                # acx, acy = 0, 0 in preparation for the next Moving Object (i)

        # After values of all moving objects have been updated,
        # data holds the new values for the next dt simulation
        data = update

    # Temporary Code to Save results of simulation in a file.
    a = pd.DataFrame(data)
    s = title + ".xlsx"
    a.to_excel(s, index=False)
    print("done")


if __name__ == '__main__':
    main()