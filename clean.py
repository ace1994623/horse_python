import csv
import math
import os
import sys


def get_data(file_name):
    file = open(file_name, "r")
    return csv.reader(file)


def check_distance(x, y, pre_x, pre_y, body_x, body_y, pre_body_x, pre_body_y, scale):
    current = math.sqrt(pow(scale * (float(x) - float(body_x)), 2) + pow(scale * (float(y) - float(body_y)), 2))
    past = math.sqrt(pow(float(pre_x) - float(pre_body_x), 2) + pow(float(pre_y) - float(pre_body_y), 2))
    #    current = scale * (float(x) - float(body_x)) + scale * (float(y) - float(body_y))
    #    past = float(pre_x) - float(pre_body_x) + float(pre_y) - pre_body_y
    print(abs((current - past) / past))
    return abs((current - past) / past) < 10


def clean_data(file_name):
    # 标准马背到屁股的距离
    normal_back_to_butt = 400
    count = 0
    direction = 0
    cleaned_data = []
    last_data = []
    csv_data = get_data(file_name)
    standard_data = []
    max_likelihood = 0
    ''' 1-3 nose
        4-6 eye
        7-9 bodyUpper
        10-12 butt
        13-21 LF
        22-30 RF
        31-39 LB
        40-48 RB'''

    # 先找出标准帧
    for item in csv_data:
        if not standard_data:
            standard_data = item
        sum_likelihood = 0
        if count > 2:
            scale = normal_back_to_butt / math.sqrt(
                pow(float(item[7]) - float(item[10]), 2) + pow(float(item[8]) - float(item[11]), 2))
            if scale > 5:
                count += 1
                continue
            index = 3
            while index < len(item):
                if index % 3 == 0:
                    sum_likelihood += float(item[index])
                index += 3
            if sum_likelihood > max_likelihood:
                max_likelihood = sum_likelihood
                for i in range(1, len(item)):
                    standard_data[i] = float(item[i]) * scale
        count += 1

    csv_data = get_data(file_name)
    count = 0
    for item in csv_data:
        # 舍弃csv中前3行
        new_record = []
        if count > 2:
            # 根据马背到屁股的距离算出比例
            scale = normal_back_to_butt / math.sqrt(
                pow(float(item[7]) - float(item[10]), 2) + pow(float(item[8]) - float(item[11]), 2))
            if scale > 5 or scale < 0.6:
                continue
            if not last_data:
                last_data.append(0)
                for i in range(1, len(item)):
                    if (i % 3) == 0:
                        last_data.append(float(item[i]))
                    else:
                        last_data.append(float(item[i]) * scale)
            # 判断朝向，向右为正，向左为负
            if direction == 0:
                if float(item[1]) > float(item[10]):
                    direction = 1
                else:
                    direction = -1
            # 舍弃第0列
            index = 1
            while index < len(item):
                availability = True
                # 如果是背，则看likely hood
                if index == 7:
                    if float(item[9]) < 0.8:
                        availability = False
                else:
                    # 如果是上半身，则先看是否比腿高，而后看和背的相对距离
                    if index <= 12:
                        if float(item[index + 1]) > float(item[14]):
                            availability = False
                    # 如果是腿，则先看是否比后背高，而后看和背的相对距离
                    else:
                        if float(item[index + 1]) < float(item[8]):
                            availability = False
                    if availability:
                        # 如果相对距离合适，但是likely hood太低也抛弃
                        if index <= 15 or index == 22:
                            availability = check_distance(item[index], item[index + 1], standard_data[index],
                                                            standard_data[index + 1], last_data[7], last_data[8],
                                                            standard_data[7], standard_data[8], scale)
                        elif index == 31 or index == 40:
                            availability = check_distance(item[index], item[index + 1], standard_data[index],
                                                            standard_data[index + 1], last_data[10],
                                                            last_data[11], standard_data[10], standard_data[11], scale)
                        else:
                            availability = check_distance(item[index], item[index + 1],
                                                            standard_data[index],
                                                            standard_data[index + 1], last_data[index - 3],
                                                            last_data[index - 2], standard_data[index - 3],
                                                            standard_data[index - 2], scale)
#                        if avail_distance:
#                            if float(item[index + 2]) < 0.01:
#                                print("2222")
#                                availability = False
#                       else:
#                            print("1111")
#                            availability = False
                # 如果可以采用则更新，否则按照上一次的坐标
                for update in range(0, 3):
                    if availability:
                        last_data[index] = float(item[index]) * scale
                    if update < 2:
                        if update == 0:
                            new_record.append(last_data[index] * direction)
                        else:
                            new_record.append(last_data[index])
                    index += 1
        count += 1
        if new_record:
            cleaned_data.append(new_record)
    return cleaned_data


def make_dir(records, file_name):
    split_point = file_name.rindex("\\")
    new_dir = file_name[0:split_point] + "\\cleaned\\"
    new_name = "cleaned_" + file_name[split_point + 1:]
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_file = open(new_dir + new_name, "w", newline="")
    writer = csv.writer(new_file)
    for data in records:
        writer.writerow(data)


file_name = str(sys.argv[1])
split_point = file_name.rindex("\\")
current_dir = file_name[0:split_point] + "\\"
for i in range(1, 76):
    if i != 15:
        current_name = str(i) + file_name[split_point + 2:]
        make_dir(clean_data(current_dir + current_name), current_dir + current_name)
