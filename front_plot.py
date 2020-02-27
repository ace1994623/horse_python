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
    # 标准马头到鼻子的距离
    normal_head_to_nose = 200
    count = 0
    filtered_data = []
    print(file_name)
    csv_data = get_data(file_name)
    for item in csv_data:
        new_record_x = []
        new_record_y = []
        # 舍弃csv中前3行
        if count > 2:
            # 根据马头到鼻子的距离算出比例
            scale = normal_head_to_nose / math.sqrt(
                pow(float(item[1]) - float(item[4]), 2) + pow(float(item[2]) - float(item[5]), 2))
            chest_x = float(item[7]) * scale
            chest_y = float(item[8]) * scale
            # 舍弃第0列
            index = 1
            #分别添加x轴和y轴数据
            while index < len(item):
                for update in range(0, 2):
                    if update == 0:
                        new_record_x.append(chest_x - float(item[index]) * scale)
                    else:
                        new_record_y.append(chest_y - float(item[index]) * scale)
                    index += 1
                index += 1
        count += 1
        if new_record_x:
            filtered_data.append(new_record_x)
            filtered_data.append(new_record_y)
    return filtered_data


# 数据标准化并计算统计相关数据
def normalize_data(filtered_data):
    result = []
    nose = []
    head = []
    lf = []
    rf = []
    record_x = []
    record_y = []
    dis_to_lf = []
    dis_to_rf = []
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
        head.append(y_data[0])
        nose.append(y_data[1])
        lf.append(y_data[3])
        rf.append(y_data[4])
    # 求均值和标准差
    nose_mean = np.mean(nose)
    head_mean = np.mean(head)
    lf_mean = np.mean(lf)
    rf_mean = np.mean(rf)
    nose_std = np.std(nose, ddof=1)
    head_std = np.std(head, ddof=1)
    lf_std = np.std(lf, ddof=1)
    rf_std = np.std(rf, ddof=1)
    # 去除异常点
    abnormal = []
    count = 0
    for i in range(0, len(nose)):
        if abs(nose[i] - nose_mean) > 3*nose_std or abs(head[i] - head_mean) > 3*head_std or abs(lf[i] - lf_mean) > 3*lf_std or abs(rf[i] - rf_mean) > 3*rf_std:
            abnormal.append(i)
    for ab_index in abnormal:
        nose.pop(ab_index-count)
        head.pop(ab_index-count)
        lf.pop(ab_index-count)
        rf.pop(ab_index-count)
        record_x.pop(ab_index-count)
        record_y.pop(ab_index-count)
        count += 1

    # 数据标准化
    nose_max = max(nose)
    nose_min = min(nose)
    head_max = max(head)
    head_min = min(head)
    lf_max = max(lf)
    lf_min = min(lf)
    rf_max = max(rf)
    rf_min = min(rf)
    for i in range(0, len(nose)):
        temp = []
#        nose[i] = (nose[i] - nose_min) / (nose_max - nose_min)
#        head[i] = (head[i] - head_min) / (head_max - head_min)
#        lf[i] = (lf[i] - lf_min) / (lf_max - lf_min)
#        rf[i] = (rf[i] - rf_min) / (rf_max - rf_min)
        # 分别计算马头与两腿的距离
        dis_to_lf.append(head[i] - lf[i])
        dis_to_rf.append(head[i] - rf[i])
        temp.append(nose[i])
        temp.append(head[i])
        temp.append(lf[i])
        temp.append(rf[i])
        temp.append(dis_to_lf[i])
        temp.append(dis_to_rf[i])
        result.append(temp)
    return result


def make_dir(records, file_name):
    header = ["nose", "head", "lf", "rf", "dis_to_lf", "dis_to_rf"]
    split_point = file_name.rindex("\\")
    new_dir = file_name[0:split_point] + "\\cleaned\\"
    new_name_y = "Y_cleaned_" + file_name[split_point + 1:]
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_file_y = open(new_dir + new_name_y, "w", newline="")
    writer_y = csv.writer(new_file_y)
    writer_y.writerow(header)
    index = 0
    while index < len(records):
        writer_y.writerow(records[index])
        index += 1


file_name = str(sys.argv[1])
split_point = file_name.rindex("\\")

# 跑模型数据
new_dir = file_name[0:split_point]
files = os.listdir(new_dir)
for file in files:
    if not os.path.isdir(new_dir + "\\" + file):
        print(file)
        normalized_data = normalize_data(filter_data(new_dir + "\\" + file))
        make_dir(normalized_data, new_dir + "\\" + file)
