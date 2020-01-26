import csv
import sys


def get_data():
    file_name = str(sys.argv[1])
    file = open(file_name, "r")
    return csv.reader(file)


def check_distance(x,y,pre_x,pre_y, threhold):




def clean_data():
    count = 0
    direction = 0
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    cleaned_data = []
    csv_data = get_data()
    last_data = []
    for item in csv_data:
        '''舍弃csv中前三行'''
        if count > 2:
            '''判断朝向，向左为正，向右为负'''
            if direction == 0:
                if item[1] > item[10]:
                    direction = 1
                else:
                    direction = -1
            '''判断是否有上一条数据'''
            if not last_data:
                last_data = item[1:]
            '''舍弃第0列'''
            index = 1
            while index < len(item):
                availability = True
                if index == 7:
                    if int(item[9]) > 0.8:

                if index <= 12:
                    if item[index+1] < last_data[14]:
                        availability = False
                        continue
                elif index <= 30:
                    if item[index+1] > last_data[7]

        count += 1

clean_data()


