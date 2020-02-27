import csv
import math
import os
import sys
import numpy as np


# 读取文件
def get_data(file_name):
    file = open(file_name, "r")
    return csv.reader(file)


# 筛选出有用数据
def filter_data(file_name):
    count = 0
    filtered_data = []
    csv_data = get_data(file_name)
    for item in csv_data:
        new_record_x = []
        new_record_y = []
        # 舍弃csv中前3行
        if count > 2:
            back_x = float(item[7])
            back_y = float(item[8])
            # 舍弃第0列
            index = 1
            #分别添加x轴和y轴数据
            # 只看前13行，鼻子，眼睛，肩胛骨和屁股
            while index < 13:
                if(float(item[index+2]) > 0.01):
                    for update in range(0, 2):
                        if update == 0:
                            new_record_x.append(back_x - float(item[index]))
                        else:
                            new_record_y.append(back_y - float(item[index]))
                        index += 1
                    index += 1
                else:
                    # 如果likelyhood低则直接忽略该项
                    new_record_x.append(" ")
                    new_record_y.append(" ")
                    index += 3
        count += 1
        if new_record_x:
            filtered_data.append(new_record_x)
            filtered_data.append(new_record_y)
    return filtered_data


# 数据标准化并计算统计相关数据
def normalize_data(filtered_data):
    result = []
    unclean_nose = []
    unclean_eye = []
    unclean_butt = []
    record_x = []
    record_y = []
    # 分别提取x，y轴数据
    index = 0
    while index < len(filtered_data):
        for update in range(0, 2):
            if update == 0:
                record_x.append(filtered_data[index])
            else:
                record_y.append(filtered_data[index])
            index += 1
    for y_data in record_y:
        if y_data[1] is not " ":
            unclean_nose.append(y_data[1])
        if y_data[0] is not " ":
            unclean_eye.append(y_data[0])
        if y_data[3] is not " ":
            unclean_butt.append(y_data[3])
    # 求均值和标准差
    nose_mean = np.mean(unclean_nose)
    eye_mean = np.mean(unclean_eye)
    butt_mean = np.mean(unclean_butt)
    nose_std = np.std(unclean_nose)
    eye_std = np.std(unclean_eye)
    butt_std = np.std(unclean_butt)

    # 去除异常点
    nose = []
    eye = []
    butt = []
    print(nose_std ,", ", nose_mean)
    print(eye_std, ", ", eye_mean)
    print(butt_std,", ", butt_mean)
    for i in unclean_nose:
        if abs(i - nose_mean) <= 3 * nose_std:
            nose.append(i)
    for j in unclean_eye:
        if abs(j - eye_mean) <= 3 * eye_std:
            eye.append(j)
    for k in unclean_butt:
        if abs(k - butt_mean) <= 3 * butt_std:
            butt.append(k)

# 数据标准化
    """nose_max = max(nose)
    nose_min = min(nose)
    eye_max = max(eye)
    eye_min = min(eye)
    butt_max = max(butt)
    butt_min = min(butt)
    for i in range(0,len(nose)):
        nose[i] = (nose[i] - nose_min) / (nose_max - nose_min)
    for j in range(0,len(eye)):
        eye[j] = (eye[j] - eye_min) / (eye_max - eye_min)
    for k in range(0,len(butt)):
        butt[k] = (butt[k] - butt_min) / (butt_max - butt_min)"""
    # 计算统计学数据

    for i in range (0,len(record_y)):
        temp = []
        if i >= len(nose):
            temp.append(" ")
        else:
            temp.append(nose[i])
        if i >= len(eye):
            temp.append(" ")
        else:
            temp.append(eye[i])
        if i >= len(butt):
            temp.append(" ")
        else:
            temp.append(butt[i])
        result.append(temp)
    return result


def make_dir(records, file_name):
    header = ["nose", "eye", "butt"]
    split_point = file_name.rindex("\\")
    new_dir = file_name[0:split_point] + "\\cleaned\\"
    new_name_y = "Y_cleaned_" + file_name[split_point + 1:]
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_file_y = open(new_dir + new_name_y, "w", newline="")
    writer_y = csv.writer(new_file_y)
    index = 0
    writer_y.writerow(header)
    while index < len(records):
        writer_y.writerow(records[index])
        index += 1


file_name = str(sys.argv[1])
split_point = file_name.rindex("\\")
new_dir = file_name[0:split_point + 1]

origin_name = file_name[split_point + 1:]
common_point = origin_name.index("D")
for i in range(1,60):
    if i != 15:
        new_name = new_dir + str(i) + origin_name[common_point:]
        print(new_name)
        normalized_data = normalize_data(filter_data(new_name))
        make_dir(normalized_data, new_name)