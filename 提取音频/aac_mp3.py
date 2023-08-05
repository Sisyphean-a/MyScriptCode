import os
import moviepy.editor as mp
from multiprocessing import Pool
from moviepy.editor import *


# 把后缀改成mp4
def convert_to_mp4(folder):

    for filename in os.listdir(folder):
        if filename.endswith('.mp3') or filename.endswith('.m4a') or filename.endswith('.aac'):
            mp4_name = filename.replace(filename.split('.')[-1], 'mp4') 
            mp4_path = os.path.join(folder, mp4_name)
            # 检查目标mp4文件是否存在
            if os.path.exists(mp4_path):
                print(f'{mp4_name} already exists, skipping...')
                continue
            # 目标文件不存在,执行重命名 
            os.rename(os.path.join(folder, filename), mp4_path)


# 获取所有的mp4文件
def get_audio_files(folder):
    files = []
    for filename in os.listdir(folder):
        if filename.endswith('.mp4'):
            files.append(os.path.join(folder, filename))
    return files


def extract_audio(video_file):
    if not os.path.exists(video_file) or not video_file.endswith('.mp4'):
        return

    try:
        video = mp.VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(video_file.replace('.mp4', '.mp3'))
        os.remove(video_file)
    except Exception as e:
        print(f'Error processing {video_file}: {e}')
        pass


def convert_to_mp3(filename):

    # 先试图使用 VideoFileClip 打开
    try:
        video = VideoFileClip(filename)

    except:
        # 打开失败,则使用 AudioFileClip 尝试读取音频
        audio = AudioFileClip(filename)
        audio.write_audiofile(filename.replace('.mp4', '.mp3'))

    else:
        # 成功打开,提取音频
        audio = video.audio
        audio.write_audiofile(filename.replace('.mp4', '.mp3'))

    # 如果原文件是 mp4 则删除
    if filename.endswith('.mp4'):
        os.remove(filename)


def main():
    folder = os.getcwd()

    convert_to_mp4(folder)
    files = [f for f in os.listdir(folder) if f.endswith('.mp4')]
    files = get_audio_files(folder)

    with Pool() as pool:
        pool.map(convert_to_mp3, files)


if __name__ == '__main__':
    main()
