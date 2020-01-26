# import necessary packages
import sys
import numpy as np
from numpy import pi, sin, cos, sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv



def get_data():
    file_name = str(sys.argv[1])
    file = open(file_name, "r")
    return csv.reader(file)


nose_x = []
nose_y = []

eye_x = []
eye_y = []

body_upper_x = []
body_upper_y = []

butt_x = []
butt_y = []

LF1_x = []
LF1_y = []
LF2_x = []
LF2_y = []
LF3_x = []
LF3_y = []

RF1_x = []
RF1_y = []
RF2_x = []
RF2_y = []
RF3_x = []
RF3_y = []

LB1_x = []
LB1_y = []
LB2_x = []
LB2_y = []
LB3_x = []
LB3_y = []

RB1_x = []
RB1_y = []
RB2_x = []
RB2_y = []
RB3_x = []
RB3_y = []

csv_data = get_data()
''' 1-3 nose
        4-6 eye
        7-9 bodyUpper
        10-12 butt
        13-21 LF
        22-30 RF
        31-39 LB
        40-48 RB'''
count = 0
for item in csv_data:
    if count > 2:
        nose_x.append(float(item[1])*-1)
        nose_y.append(float(item[2])*-1)

        eye_x.append(float(item[4])*-1)
        eye_y.append(float(item[5])*-1)

        body_upper_x.append(float(item[7])*-1)
        body_upper_y.append(float(item[8])*-1)

        butt_x.append(float(item[10])*-1)
        butt_y.append(float(item[11])*-1)

        LF1_x.append(float(item[13])*-1)
        LF1_y.append(float(item[14]) * -1)

        LF2_x.append(float(item[16])*-1)
        LF2_y.append(float(item[17]) * -1)

        LF3_x.append(float(item[19])*-1)
        LF3_y.append(float(item[20]) * -1)

        RF1_x.append(float(item[22]) * -1)
        RF1_y.append(float(item[23]) * -1)

        RF2_x.append(float(item[25]) * -1)
        RF2_y.append(float(item[26]) * -1)

        RF3_x.append(float(item[28]) * -1)
        RF3_y.append(float(item[29]) * -1)

        LB1_x.append(float(item[31]) * -1)
        LB1_y.append(float(item[32]) * -1)

        LB2_x.append(float(item[34]) * -1)
        LB2_y.append(float(item[35]) * -1)

        LB3_x.append(float(item[37]) * -1)
        LB3_y.append(float(item[38]) * -1)

        RB1_x.append(float(item[40]) * -1)
        RB1_y.append(float(item[41]) * -1)

        RB2_x.append(float(item[43]) * -1)
        RB2_y.append(float(item[44]) * -1)

        RB3_x.append(float(item[46]) * -1)
        RB3_y.append(float(item[47]) * -1)

    count += 1
# set up the figure and subplot
fig = plt.figure()
fig.canvas.set_window_title('Matplotlib Animation')
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-1920,0), ylim=(-1080, 0))
ax.grid()
body_line, = ax.plot([], [], 'o-', lw=1, color='#de2d26')
left_front_leg, = ax.plot([], [], 'o-', lw=1, color='#0000FF')
right_front_leg, = ax.plot([], [], 'o-', lw=1, color='#EE82EE')
left_rear_leg, = ax.plot([], [], 'o-', lw=1, color='#DAA520')
right_rear_leg, = ax.plot([], [], 'o-', lw=1, color='#7FFF00')


# initialization function
def init():
    body_line.set_data([], [])
    left_front_leg.set_data([], [])
    right_front_leg.set_data([], [])
    left_rear_leg.set_data([], [])
    right_rear_leg.set_data([], [])
    return body_line, left_front_leg, right_front_leg, left_rear_leg, right_rear_leg,


# animation function
def animate(i):
    x_points = [nose_x[i], eye_x[i], body_upper_x[i], butt_x[i]]
    y_points = [nose_y[i], eye_y[i], body_upper_y[i], butt_y[i]]
    body_line.set_data(x_points, y_points)

    left_front_leg_x = [body_upper_x[i], LF1_x[i], LF2_x[i], LF3_x[i]]
    left_front_leg_y = [body_upper_y[i], LF1_y[i], LF2_y[i], LF3_y[i]]
    left_front_leg.set_data(left_front_leg_x, left_front_leg_y)

    right_front_leg_x = [body_upper_x[i], RF1_x[i], RF2_x[i], RF3_x[i]]
    right_front_leg_y = [body_upper_y[i], RF1_y[i], RF2_y[i], RF3_y[i]]
    right_front_leg.set_data(right_front_leg_x, right_front_leg_y)

    left_rear_leg_x = [butt_x[i], LB1_x[i], LB2_x[i], LB3_x[i]]
    left_rear_leg_y = [butt_y[i], LB1_y[i], LB2_y[i], LB3_y[i]]
    left_rear_leg.set_data(left_rear_leg_x, left_rear_leg_y)

    right_rear_leg_x = [butt_x[i], RB1_x[i], RB2_x[i], RB3_x[i]]
    right_rear_leg_y = [butt_y[i], RB1_y[i], RB2_y[i], RB3_y[i]]
    right_rear_leg.set_data(right_rear_leg_x, right_rear_leg_y)
    return body_line, left_front_leg, right_front_leg, left_rear_leg, right_rear_leg,


# call the animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(nose_x), interval=40, blit=True, repeat=True)
## to save animation, uncomment the line below:
## ani.save('offset_piston_motion_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

# show the animation
plt.show()
