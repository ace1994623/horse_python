# import necessary packages
import sys
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
max_x = 0
max_y = 0
max_4 = 0
max_5 = 0
for item in csv_data:
        nose_x.append(float(item[0]) - float(item[4]))
        nose_y.append((float(item[1]) - float(item[5])) *-1)

        eye_x.append(float(item[2]) - float(item[4]))
        eye_y.append((float(item[3]) - float(item[5]))*-1)

        body_upper_x.append(0)
        body_upper_y.append(0)

        butt_x.append(float(item[6]) - float(item[4]))
        butt_y.append((float(item[7]) - float(item[5]))*-1)

        LF1_x.append(float(item[8]) - float(item[4]))
        LF1_y.append((float(item[9]) - float(item[5])) * -1)

        LF2_x.append(float(item[10]) - float(item[4]))
        LF2_y.append((float(item[11]) - float(item[5])) * -1)

        LF3_x.append(float(item[12]) - float(item[4]))
        LF3_y.append((float(item[13]) - float(item[5])) * -1)

        RF1_x.append(float(item[14]) - float(item[4]))
        RF1_y.append((float(item[15]) - float(item[5])) * -1)

        RF2_x.append(float(item[16]) - float(item[4]))
        RF2_y.append((float(item[17]) - float(item[5])) * -1)

        RF3_x.append(float(item[18]) - float(item[4]))
        RF3_y.append((float(item[19]) - float(item[5])) * -1)

        LB1_x.append(float(item[20]) - float(item[4]))
        LB1_y.append((float(item[21]) - float(item[5])) * -1)

        LB2_x.append(float(item[22]) - float(item[4]))
        LB2_y.append((float(item[23]) - float(item[5])) * -1)

        LB3_x.append(float(item[24]) - float(item[4]))
        LB3_y.append((float(item[25]) - float(item[5])) * -1)

        RB1_x.append(float(item[26]) - float(item[4]))
        RB1_y.append((float(item[27]) - float(item[5])) * -1)

        RB2_x.append(float(item[28]) - float(item[4]))
        RB2_y.append((float(item[29]) -float(item[5])) * -1)

        RB3_x.append(float(item[30]) - float(item[4]))
        RB3_y.append((float(item[31])- float(item[5])) * -1)
        max_x = max(max_x, float(item[0]), float(item[2]), float(item[4]), float(item[6]), float(item[8]),
                    float(item[10]), float(item[12]), float(item[14]), float(item[16]),float(item[18]),
                    float(item[20]), float(item[22]), float(item[24]), float(item[26]), float(item[28]),
                    float(item[30]))
        max_y = max(max_y, float(item[1]), float(item[3]), float(item[5]), float(item[7]), float(item[9]),
                    float(item[11]), float(item[13]), float(item[15]), float(item[17]),
                    float(item[19]), float(item[21]), float(item[23]), float(item[25]), float(item[27]),
                    float(item[29]), float(item[31]))
        max_4 = max(max_4, float(item[4]))
        max_5 = max(max_5, float(item[5]))
# set up the figure and subplot

fig = plt.figure()
fig.canvas.set_window_title('Matplotlib Animation')
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-1920/2,1920/2), ylim=(-1080/2 - 200, 1080/2 - 200))
#ax.grid()
#plt.xticks([])
#plt.yticks([])
body_line, = ax.plot([], [], 'o-', lw=1, color='#de2d26')
left_front_leg, = ax.plot([], [], 'o-', lw=1, color='#0000FF')
right_front_leg, = ax.plot([], [], 'o-', lw=1, color='#EE82EE')
left_rear_leg, = ax.plot([], [], 'o-', lw=1, color='#DAA520')
right_rear_leg, = ax.plot([], [], 'o-', lw=1, color='#7FFF00')
"""
plt.figure('Line fig')
ax = plt.gca()
#设置x轴、y轴名称
ax.set_xlabel('x')
ax.set_ylabel('y')

#画连线图，以x_list中的值为横坐标，以y_list中的值为纵坐标
#参数c指定连线的颜色，linewidth指定连线宽度，alpha指定连线的透明度
ax.plot(LF1_x, LF1_y, color='r', linewidth=1)
"""


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
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(nose_x), interval=50, blit=True, repeat=True)
## to save animation, uncomment the line below:
## ani.save('offset_piston_motion_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

# show the animation
plt.show()
