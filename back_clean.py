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
            scale = normal_left_to_right / (float(item[1]) - float(item[4]))
            # 舍弃第0列
            index = 1
            #分别添加x轴和y轴数据
            while index < len(item):
                if item[index + 2] > 0.01:
                    for update in range(0, 2):
                        if update == 0:
                            new_record_x.append(float(item[index]) * scale)
                        else:
                            new_record_y.append(float(item[index]) * scale)
                        index += 1
                    index += 1
                else:
                    new_record_y = []
                    new_record_x = []
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
    for i in range(0, len(left_butt)):
        if (abs(left_butt[i] - left_butt_mean) > 3*left_butt_std) or (abs(right_butt[i] - right_butt_mean) > 3*right_butt_std) or (abs(lr[i] - lr_mean) > 3*lr_std )or (abs(rr[i] - rr_mean) > 3*rr_std):
            abnormal.append(i)
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
        left_butt[i] = (left_butt[i] - left_butt_min) / (left_butt_max - left_butt_min)
        right_butt[i] = (right_butt[i] - right_butt_min) / (right_butt_max - right_butt_min)
        lr[i] = (lr[i] - lr_min) / (lr_max - lr_min)
        rr[i] = (rr[i] - rr_min) / (rr_max - rr_min)
        # 分别计算马头与两腿的距离
        dis_to_lr.append(left_butt[i] - lr[i])
        dis_to_rr.append(right_butt[i] - rr[i])

    # 计算统计学数据
    # 均值
    dis_to_lr_mean = np.mean(dis_to_lr)
    dis_to_rr_mean = np.mean(dis_to_rr)
    # 标准差
    dis_to_lr_std = np.std(dis_to_lr)
    dis_to_rr_std = np.std(dis_to_rr)
    # 方差
    dis_to_lr_var = np.var(dis_to_lr)
    dis_to_rr_var = np.var(dis_to_rr)
    # 偏度
    dis_to_lr_p_sum = 0
    dis_to_rr_p_sum = 0
    for i in range(0, len(left_butt)):
        dis_to_lr_p_sum += pow(dis_to_lr[i] - min(dis_to_lr), 3)
        dis_to_rr_p_sum += pow(dis_to_rr[i] - min(dis_to_rr), 3)
    dis_to_lr_pian = dis_to_lr_p_sum/(len(dis_to_lr) * pow(dis_to_lr_std, 3))
    dis_to_rr_pian = dis_to_rr_p_sum/(len(dis_to_rr) * pow(dis_to_rr_std, 3))
    result.append(dis_to_lr_mean)
    result.append(dis_to_lr_var)
    result.append(dis_to_lr_pian)
    result.append(dis_to_rr_mean)
    result.append(dis_to_rr_var)
    result.append(dis_to_rr_pian)
    result.append(" ")
    return result


"""def make_dir(records, file_name):
    split_point = file_name.rindex("\\")
    new_dir = file_name[0:split_point] + "\\cleaned\\"
    new_name_x = "X_cleaned_" + file_name[split_point + 1:]
    new_name_y = "Y_cleaned_" + file_name[split_point + 1:]
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_file_x = open(new_dir + new_name_x, "w", newline="")
    new_file_y = open(new_dir + new_name_y, "w", newline="")
    writer_x = csv.writer(new_file_x)
    writer_y = csv.writer(new_file_y)
    index = 0
    while index < len(records):
        for update in range(0, 2):
            if update == 0:
                writer_x.writerow(records[index])
            else:
                writer_y.writerow(records[index])
            index += 1"""


def make_dir(records, file_name):
    header = ["dis_to_lr_mean", "dis_to_lr_var", "dis_to_lr_pian", "dis_to_rr_mean", "dis_to_rr_var", "dis_to_rr_pian", "label"]
    #records.append(" ")
    split_point = file_name.rindex("/")
    new_dir = file_name[0:split_point + 1]
    new_name = "cleaned_" + file_name[split_point + 1:]
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_file = open(new_dir+new_name, "w", newline="")
    writer = csv.writer(new_file)
    writer.writerow(header)
    writer.writerow(records)


file_name = str(sys.argv[1])
normalized_data = normalize_data(filter_data(file_name))
make_dir(normalized_data, file_name)