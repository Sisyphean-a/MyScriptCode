import os
from cv2 import VideoCapture

video_type = ["avi", "wmv", "mpeg", "mp4", "m4v", "mov", "flv", "rmvb"]
video_path_list = []
relative_path_list = []
time_list = []


def folder_path():
    folder = input("请输入目标路径：")
    return folder


def get_file_path(folder, video_path_list, video_type):
    for path, dirs, filename in os.walk(folder):
        for file in filename:
            if file.split(".")[-1] in video_type:
                video_path_list.append(path + "\\" + file)


def get_relative_path(video_path_list, folder_name, relative_path_list):
    delete_num = len(folder_name)
    for i in video_path_list:
        relative_path_list.append(i[delete_num + 1:])


def son_path(video_path_list, son_path_list):
    for path in video_path_list:
        fragment = path.split("\\")[:-1]
        division = ""
        for cl in fragment:
            division = division + cl + "\\"
        son_path_list.append(division)


def testing(file):
    cap = VideoCapture(file)
    if cap.isOpened():
        rate = cap.get(5)
        FrameNumber = cap.get(7)
        duration = round(FrameNumber / rate / 60, 3)
        return duration


def add_time(video_path_list, time_list):
    whole_time = 0.0
    init_time_list = []
    for path_name in video_path_list:
        init_time_list.append(testing(path_name))
    for time in init_time_list:
        if isinstance(time, float):
            time = round(time, 2)
            time_list.append(time)
            whole_time = whole_time + time
    whole_time = round(whole_time, 3)
    return whole_time


def print_information(whole_time, time_list):
    n_videos = len(time_list) 
    max_time = max(time_list)  
    min_time = min(time_list)  
    total_time_minutes = whole_time  
    total_time_hours = round(whole_time / 60, 2)

    information = f"最长时长：{max_time}分钟\n" \
                  f"最短时长：{min_time}分钟\n" \
                  f"视频数量：{n_videos}个\n" \
                  f"总时长：{total_time_minutes}分钟\n" \
                  f"总时长：{total_time_hours}小时\n\n\n"
    print(information) 
    return information


def export_txt(folder, dict, information):
    export_path = folder + "\\video_time.txt"
    with open(export_path, "w") as f:
        f.write(information)
        f.write("  ------------------------------------------------------------------\n")
        for k, v in dict.items():
            name = k.replace(u'\xa0', u'')
            time = pad_string(str(v))
            string = f"    time:{time}    {name}\n"
            parting_line = generate_separator(string)
            f.write(f"{string}  --------------{parting_line}\n")


def pad_string(input_str):
    length = len(input_str)
    if length < 7:
        spaces = " " * (7 - length)
        input_str += spaces
    return input_str


def generate_separator(string):
    length = len(string)
    separator = "-" * length
    return separator


def one_time_or_path(folder):
    video_path_list = []
    relative_path_list = []
    time_list = []
    get_file_path(folder, video_path_list, video_type)
    get_relative_path(video_path_list, folder, relative_path_list)
    whole_time = add_time(video_path_list, time_list)
    information = print_information(whole_time, time_list)
    dicta = dict(zip(relative_path_list, time_list))
    export_txt(folder, dicta, information)

    return information


def many_time_or_path(folder, son_path_list=None):
    if son_path_list is None:
        son_path_list = []
    get_file_path(folder, video_path_list, video_type)
    son_path_list.append(folder)
    son_path(video_path_list, son_path_list)
    son_path_list = list(set(son_path_list))
    for i in son_path_list:
        print(i)
        one_time_or_path(i)


if __name__ == "__main__":
    folder = folder_path()
    many_time_or_path(folder)

