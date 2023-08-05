import os
from cv2 import VideoCapture

video_type = ["avi", "wmv", "mpeg", "mp4", "m4v", "mov", "flv", "rmvb"]

def folder_path():
    return input("请输入目标路径：")

def get_video_paths(folder):
    video_paths = []
    for path, dirs, files in os.walk(folder):
        for file in files:
            if file.split(".")[-1] in video_type:
                video_paths.append(os.path.join(path, file))
    return video_paths

def get_video_duration(file):
    cap = VideoCapture(file)
    if cap.isOpened():
        rate = cap.get(5)
        frame_number = cap.get(7)
        duration = round(frame_number / rate / 60, 3)
        return duration

def get_video_durations(video_paths):
    durations = []
    total_duration = 0.0
    for path in video_paths:
        duration = get_video_duration(path)
        if isinstance(duration, float):
            duration = round(duration, 2)
            durations.append(duration)
            total_duration += duration
    total_duration = round(total_duration, 3)
    return durations, total_duration

def print_information(durations, total_duration):
    n_videos = len(durations) 
    max_time = max(durations)  
    min_time = min(durations)  
    total_time_minutes = total_duration  
    total_time_hours = round(total_duration / 60, 2)

    information = f"最长时长：{max_time}分钟\n" \
                  f"最短时长：{min_time}分钟\n" \
                  f"视频数量：{n_videos}个\n" \
                  f"总时长：{total_time_minutes}分钟\n" \
                  f"总时长：{total_time_hours}小时\n\n\n"
    print(information) 
    return information

def export_txt(folder, video_paths, durations, information):
    export_path = os.path.join(folder, "video_time.txt")
    with open(export_path, "w") as f:
        f.write(information)
        f.write("  ------------------------------------------------------------------\n")
        for path, duration in zip(video_paths, durations):
            name = path.replace(u'\xa0', u'')
            time = pad_string(str(duration))
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

def process_folder(folder):
    video_paths = get_video_paths(folder)
    durations, total_duration = get_video_durations(video_paths)
    information = print_information(durations, total_duration)
    export_txt(folder, video_paths, durations, information)
    subfolders = [os.path.join(folder, d) for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]
    for subfolder in subfolders:
        process_folder(subfolder)

if __name__ == "__main__":
    folder = folder_path()
    process_folder(folder)

