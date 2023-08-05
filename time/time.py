from cv2 import VideoCapture
import os

# 常见视频种类
video_type=["avi","wmv","mpeg","mp4","m4v","mov","flv","rmvb"]
# 视频绝对路径列表
video_path_list = []
# 视频相对路径列表
relative_path_list = []
# 获取视频所在路径列表
son_path_list = []
# 视频时长列表
time_list = []

# 读取目标路径
def folder_path():
    folder = input("请输入目标路径：")
    return folder

# 获取视频绝对路径列表
def get_file_path(folder,video_path_list,video_type):
    for path,dirs,filename in os.walk(folder):
        for file in filename:
            if file.split(".")[-1] in video_type:
                video_path_list.append(path + "\\" +file)

# 获取视频相对路径列表
def get_relative_path(video_path_list,folder_name,relative_path_list):
    delete_num = len(folder_name)
    for i in video_path_list:
        relative_path_list.append(i[delete_num+1:])

# 获取视频所在路径列表
def son_path(video_path_list,son_path_list):
    for path in video_path_list:
        fragment = path.split("\\")[:-1]
        division = ""
        for cl in fragment:
            division = division + cl + "\\"
        son_path_list.append(division)
    
# 通过路径获取单个视频时长
def testing(file):
    cap = VideoCapture(file)
    if cap.isOpened():
        rate = cap.get(5)
        FrameNumber = cap.get(7)
        duration = round(FrameNumber/rate/60,3)
        return duration

# 获取视频时长列表以及总时间
def add_time(video_path_list,time_list):
    whole_time = 0.0
    init_time_list = []
    for path_name in video_path_list:
        init_time_list.append(testing(path_name)) 
    for time in init_time_list:
        if isinstance(time,float):
            time = round(time,2)
            time_list.append(time)
            whole_time = whole_time + time
    whole_time = round(whole_time,3)
    return whole_time

# 输出视频信息
def print_information(whole_time,time_list):
    information = ("最长时长：" + str(max(time_list)) + "分钟\n"
                "最短时长：" + str(min(time_list)) + "分钟\n"
                "视频数量：" + str(len(time_list)) + "个\n"
                "总时长：" + str(whole_time) + "分钟\n"
                "总时长：" + str(round(whole_time/60,2)) + "小时\n\n\n")
    print(information)
    return information

# 导出视频信息文件
def export_txt(folder,dict,information):
    export_path = folder + "\\video_time.txt"
    with open(export_path,"w") as f:
        f.write(information)
        for k,v in dict.items():
            f.write(k.replace(u'\xa0', u'')+"\n")
            f.write("   time:" +str(v) + "\n")

# 主要运行函数
def time_or_path(folder,video_path_list,relative_path_list,time_list):
    get_file_path(folder,video_path_list,video_type)
    get_relative_path(video_path_list,folder,relative_path_list)
    whole_time = add_time(video_path_list,time_list)
    # 输出视频信息
    information = print_information(whole_time,time_list)
    dicta = dict(zip(relative_path_list,time_list))
    export_txt(folder,dicta,information)

# 程序入口
if __name__ == "__main__":
    folder = folder_path()
    #folder = "E:\Python Flask"
    get_file_path(folder,video_path_list,video_type)
    son_path_list.append(folder)
    son_path(video_path_list,son_path_list)
    son_path_list = list(set(son_path_list))
    for i in son_path_list:
        video_path_list = []
        relative_path_list = []
        time_list = []
        print(i)
        time_or_path(i,video_path_list,relative_path_list,time_list)
