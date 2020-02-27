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
    # 标准马背到屁股的距离
    normal_back_to_butt = 354
    count = 0
    filtered_data = []
    csv_data = get_data(file_name)
    for item in csv_data:
        new_record_x = []
        new_record_y = []
        # 舍弃csv中前3行
        if count > 2:
            # 根据马背到屁股的距离算出比例
            scale = normal_back_to_butt / math.sqrt(
                pow(float(item[7]) - float(item[10]), 2) + pow(float(item[8]) - float(item[11]), 2))
            back_x = float(item[7]) * scale
            back_y = float(item[8]) * scale
            # 舍弃第0列
            index = 1
            #分别添加x轴和y轴数据
            while index < len(item):
                for update in range(0, 2):
                    if update == 0:
                        new_record_x.append(back_x - float(item[index]) * scale)
                    else:
                        new_record_y.append(back_y - float(item[index]) * scale)
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
    eye = []
    butt = []
    lf = []
    rf = []
    lr = []
    rr = []
    lf_x = []
    rf_x = []
    lr_x = []
    rr_x = []
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
        nose.append(y_data[1])
        eye.append(y_data[0])
        butt.append(y_data[3])
        lf.append(y_data[5])
        rf.append(y_data[7])
        lr.append(y_data[9])
        rr.append(y_data[11])
    for x_data in record_x:
        lf_x.append(x_data[5])
        rf_x.append(x_data[7])
        lr_x.append(x_data[9])
        rr_x.append(x_data[11])
    # 求均值和标准差
    nose_mean = np.mean(nose)
    eye_mean = np.mean(eye)
    butt_mean = np.mean(butt)
    lf_mean = np.mean(lf)
    rf_mean = np.mean(rf)
    lr_mean = np.mean(lr)
    rr_mean = np.mean(rr)
    nose_std = np.std(nose)
    eye_std = np.std(eye)
    butt_std = np.std(butt)
    lf_std = np.std(lf)
    rf_std = np.std(rf)
    lr_std = np.std(lr)
    rr_std = np.std(rr)
    # 去除异常点
    # \
    #                 or (lf[i] - lf_mean) > 3*lf_std or (rf[i] - rf_mean) > 3*rf_std \
    #                 or (lr[i] - lr_mean) > 3*lr_std or (rr[i] - rr_mean) > 3*rr_std
    abnormal = []
    count = 0
    for i in range(0, len(nose)):
        if (nose[i] - nose_mean) > 3*nose_std or (eye[i] - eye_mean) > 3*eye_std or (butt[i] - butt_mean) > 3*butt_std:
            abnormal.append(i)
    for ab_index in abnormal:
        nose.pop(ab_index-count)
        eye.pop(ab_index-count)
        butt.pop(ab_index-count)
        lf.pop(ab_index-count)
        rf.pop(ab_index-count)
        lr.pop(ab_index-count)
        rr.pop(ab_index-count)
        record_x.pop(ab_index-count)
        record_y.pop(ab_index-count)
        count +=1
    # 找到四只脚以及马头和屁股的所有局部最低点



    # 数据标准化
    nose_max = max(nose)
    nose_min = min(nose)
    eye_max = max(eye)
    eye_min = min(eye)
    butt_max = max(butt)
    butt_min = min(butt)
    for i in range(0, len(nose)):
        nose[i] = (nose[i] - nose_min) / (nose_max - nose_min)
        eye[i] = (eye[i] - eye_min) / (eye_max - eye_min)
        butt[i] = (butt[i] - butt_min) / (butt_max - butt_min)
    # 计算统计学数据
    # 均值
    nose_mean = np.mean(nose)
    eye_mean = np.mean(eye)
    butt_mean = np.mean(butt)
    # 标准差
    nose_std = np.std(nose)
    eye_std = np.std(eye)
    butt_std = np.std(butt)
    # 方差
    nose_var = np.var(nose)
    eye_var = np.var(eye)
    butt_var = np.var(butt)
    # 偏度
    nose_p_sum = 0
    eye_p_sum = 0
    butt_p_sum = 0
    for i in range(0, len(nose)):
        nose_p_sum += pow(nose[i] - min(nose), 3)
        eye_p_sum += pow(eye[i] - min(eye), 3)
        butt_p_sum += pow(butt[i] - min(butt), 3)
    nose_pian = nose_p_sum/(len(nose) * pow(nose_std, 3))
    eye_pian = eye_p_sum/(len(eye) * pow(eye_std, 3))
    butt_pian = butt_p_sum/(len(butt) * pow(butt_std, 3))
    result.append(nose_mean)
    result.append(nose_var)
    result.append(nose_pian)
    result.append(eye_mean)
    result.append(eye_var)
    result.append(eye_pian)
    result.append(butt_mean)
    result.append(butt_var)
    result.append(butt_pian)
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
    header = ["nose_mean", "nose_var", "nose_pian", "eye_mean", "eye_var", "eye_pian", "butt_mean", "butt_var", "butt_pian", "label"]
    #records.append(" ")
    split_point = file_name.rindex("\\")
    new_dir = file_name[0:split_point + 1]
    new_name = "cleaned_" + file_name[split_point + 1:]
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_file = open(new_dir+new_name, "w", newline="")
    writer = csv.writer(new_file)
    writer.writerow(header)
    for record in records:
        writer.writerow(record)


results = []
file_name = str(sys.argv[1])
split_point = file_name.rindex("\\")
new_dir = file_name[0:split_point + 1]

origin_name = file_name[split_point + 1:]
common_point = origin_name.index("D")
for i in range(1,75):
    if i != 15:
        new_name = new_dir + str(i) + origin_name[common_point:]
        print(new_name)
        print(results)
        normalized_data = normalize_data(filter_data(new_name))
        results.append(normalized_data)
make_dir(results, file_name)
