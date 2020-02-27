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
    # 标准左屁股到右屁股x轴的距离
    #TODO: 找到合适的值
    normal_left_to_right = 239
    count = 0
    filtered_data = []
    csv_data = get_data(file_name)
    for item in csv_data:
        new_record_x = []
        new_record_y = []
        # 舍弃csv中前3行
        if count > 2:
            # 根据左屁股到右屁股x轴的距离算出比例
            scale = normal_left_to_right / abs(float(item[1]) - float(item[4]))
            # 舍弃第0列
            index = 1
            #分别添加x轴和y轴数据
            while index < len(item):
                if(float(item[index +2]) > 0.01):
                    for update in range(0, 2):
                        if update == 0:
                            new_record_x.append(float(item[index]) * scale)
                        else:
                            new_record_y.append(float(item[index]) * scale * -1)
                        index += 1
                    index += 1
                else:
                    new_record_x = []
                    new_record_y = []
                    break
        count += 1
        if new_record_x:
            filtered_data.append(new_record_x)
            filtered_data.append(new_record_y)
    return filtered_data


# 数据标准化并计算统计相关数据
def normalize_data(filtered_data):
    result = []
    left_butt = []
    right_butt = []
    lr = []
    rr = []
    record_x = []
    record_y = []
    dis_to_lr = []
    dis_to_rr = []
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
        left_butt.append(y_data[0])
        right_butt.append(y_data[1])
        lr.append(y_data[2])
        rr.append(y_data[3])
    # 求均值和标准差
    left_butt_mean = np.mean(left_butt)
    right_butt_mean = np.mean(right_butt)
    lr_mean = np.mean(lr)
    rr_mean = np.mean(rr)
    left_butt_std = np.std(left_butt)
    right_butt_std = np.std(right_butt)
    lr_std = np.std(lr)
    rr_std = np.std(rr)
    # 去除异常点
    abnormal = []
    count = 0
    print(left_butt_mean)
    print(left_butt_std)
    for i in range(0, len(left_butt)):
        if (abs(left_butt[i] - left_butt_mean) > 3*left_butt_std) or (abs(right_butt[i] - right_butt_mean) > 3*right_butt_std) or (abs(lr[i] - lr_mean) > 3*lr_std )or (abs(rr[i] - rr_mean) > 3*rr_std):
            abnormal.append(i)
    print(abnormal)
    for ab_index in abnormal:
        left_butt.pop(ab_index-count)
        right_butt.pop(ab_index-count)
        lr.pop(ab_index-count)
        rr.pop(ab_index-count)
        record_x.pop(ab_index-count)
        record_y.pop(ab_index-count)
        count +=1

    # 数据标准化
    left_butt_max = max(left_butt)
    left_butt_min = min(left_butt)
    right_butt_max = max(right_butt)
    right_butt_min = min(right_butt)
    lr_max = max(lr)
    lr_min = min(lr)
    rr_max = max(rr)
    rr_min = min(rr)

    for i in range(0, len(left_butt)):
        # 分别计算马头与两腿的距离
        temp = []
        left_butt[i] = (left_butt[i] - left_butt_min) / (left_butt_max - left_butt_min)
        right_butt[i] = (right_butt[i] - right_butt_min) / (right_butt_max - right_butt_min)
        lr[i] = (lr[i] - lr_min) / (lr_max - lr_min)
        rr[i] = (rr[i] - rr_min) / (rr_max - rr_min)
        dis_to_lr.append(left_butt[i] - lr[i])
        dis_to_rr.append(right_butt[i] - rr[i])
        temp.append(left_butt[i])
        temp.append(right_butt[i])
        temp.append(lr[i])
        temp.append(rr[i])
        temp.append(dis_to_lr[i])
        temp.append(dis_to_rr[i])
        result.append(temp)
    return result


def make_dir(records, file_name):
    split_point = file_name.rindex("\\")
    header = ["left_butt", "right_butt", "lr", "rr", "dis_to_lr", "dis_to_rr"]
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



results = []
file_name = str(sys.argv[1])
split_point = file_name.rindex("\\")

# 跑模型数据
new_dir = file_name[0:split_point]
files = os.listdir(new_dir)
for file in files:
    if not os.path.isdir(new_dir + "\\" + file):
        normalized_data = normalize_data(filter_data(new_dir + "\\" + file))
        make_dir(normalized_data, new_dir + "\\" + file)
