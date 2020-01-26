import csv
import math
import sys


def get_data():
    file_name = str(sys.argv[1])
    file = open(file_name, "r")
    return csv.reader(file)


def check_distance(x, y, pre_x, pre_y, pre_body_x, pre_body_y, body_x, body_y, scale):
    current = math.sqrt(pow(scale * (float(x) - float(body_x)), 2) + pow(scale * (float(y) - float(body_y)), 2))
    print(current)
    past = math.sqrt(pow(float(pre_x) - float(pre_body_x), 2) + pow(float(pre_y) - float(pre_body_y), 2))
    print(past)
    return abs(current - past) < 100


def clean_data():
    # 标准马背到屁股的距离
    normal_back_to_butt = 400
    count = 0
    direction = 0
    cleaned_data = []
    last_data = []
    csv_data = get_data()
    ''' 1-3 nose
        4-6 eye
        7-9 bodyUpper
        10-12 butt
        13-21 LF
        22-30 RF
        31-39 LB
        40-48 RB'''
    for item in csv_data:
        ignore = False
        # 舍弃csv中前三行
        new_record = []
        if count > 2:
            print(item)
            # 根据马背到屁股的距离算出比例
            scale = normal_back_to_butt / math.sqrt(
                pow(float(item[7]) - float(item[10]),2) + pow(float(item[8]) - float(item[11]), 2))
            if not last_data:
                for i in range(1, len(item)):
                    if (i % 3) == 0:
                        last_data.append(float(item[i]))
                    else:
                        last_data.append(float(item[i]) * scale)
            # 判断朝向，向左为正，向右为负
            if direction == 0:
                if float(item[1]) > float(item[10]):
                    direction = 1
                else:
                    direction = -1
            # 舍弃第0列
            index = 1
            while index < len(item):
                print(index)
                availability = True
                # 如果是背，则看likely hood
                if index == 7:
                    if float(item[9]) < 0.8:
                        print("!!!!!!!!1")
                        availability = False
                else:
                    # 如果是上半身，则先看是否比腿高，而后看和背的相对距离
                    if index <= 12:
                        if float(item[index + 1]) < float(last_data[14]):
                            print("!!!!2")
                            availability = False
                    # 如果是腿，则先看是否比后背高，而后看和背的相对距离
                    else:
                        if float(item[index + 1]) > float(last_data[8]):
                            print("!!!!3")
                            availability = False
                    if availability:
                        # 如果相对距离合适，但是likely hood太低也抛弃
                        if check_distance(item[index], item[index + 1], last_data[index], item[7], item[8], last_data[index + 1], last_data[7], last_data[8], scale):
                            if float(item[index + 2]) < 0.5:
                                print("!!!!4")
                                availability = False
                        else:
                            print("!!!!5")
                            availability = False
                if index <= 12 and not availability:
                    ignore = True
                    break
                # 如果可以采用则更新，否则按照上一次的坐标
                for update in range(0, 3):
                    index += 1
                    if availability:
                        new_record.append(float(item[index + update]) * scale)
                        last_data[index + update] = float(item[index + update]) * scale
                    else:
                        new_record.append(float(item[index + update]))
        count += 1
        if new_record and not ignore:
            cleaned_data.append(new_record)
    return cleaned_data


clean_data()
