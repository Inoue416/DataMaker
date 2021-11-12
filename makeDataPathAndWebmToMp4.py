import os
import glob
import re
import shutil

ROOT = os.getcwd()

def get_data_path(path):
    data = glob.glob(path+'/*')
    return data

"""def back_dir():
    os.chdir('../')
    return

def change_dir(path):
    os.chdir(path)"""

def webm_to_mp4(path, filename):
    cmd = "ffmpeg -i {} {}".format(path, os.path.join(ROOT, filename))
    os.system(cmd)

def is_dir(path):
    if not os.path.isdir(path):
        #print(os.getcwd())
        os.mkdir(path)

# TODO: make frames code
def make_frames(path, save_path):
    #print(glob.glob(save_path))
    if glob.glob(save_path+'/*') != []:
        print('skip because exist.')
        return
    cmd = "ffmpeg -i {} -r 30 {}/%03d.jpg".format(path, save_path)
    print(cmd)
    os.system(cmd)
    return

def extract_voice(path, save_path):
    if glob.glob(save_path) != []:
        print('skip because exist.')
        #exit()
        return
    cmd = "ffmpeg -i {} -f mp3 {}".format(path, save_path)
    os.system(cmd)
    #exit()
    return

def make_dataPath(type):
    print('----- START -----')
    print('{}フォルダの処理を行います。'.format(type))
    path_list = []
    frame_list = []
    voice_list = []
    is_dir(os.path.join(ROOT, 'videos'))
    is_dir(os.path.join(ROOT, 'frames'))
    is_dir(os.path.join(ROOT, 'voices'))
    #ROOT = "./{}".format(type)
    #change_dir(ROOT)
    datapath = os.path.join(ROOT, type)
    dl = get_data_path(datapath)
    for i in range(len(dl)):
        if (dl[i].split('.'))[-1] == 'txt':
            continue
        video_path = 'videos/{}'.format(type)
        frame_folder = 'frames/{}'.format(type)
        voice_path = "voices/{}".format(type)
        is_dir(os.path.join(ROOT, video_path))
        is_dir(os.path.join(ROOT, voice_path))
        is_dir(os.path.join(ROOT, frame_folder))
        video_path = os.path.join(video_path, (dl[i].split('/'))[-1])
        frame_folder = os.path.join(frame_folder, (dl[i].split('/'))[-1])
        voice_path = os.path.join(voice_path, (dl[i].split('/'))[-1])
        is_dir(os.path.join(ROOT, frame_folder))
        is_dir(os.path.join(ROOT, video_path))
        is_dir(os.path.join(ROOT, voice_path))
        #print(text)
        #change_dir(dl[i])
        data = get_data_path(os.path.join(ROOT, dl[i]))
        buff_video = video_path
        buff_frame = frame_folder
        buff_voice = voice_path
        for a in range(len(data)):
            #print('data[{}]: {}'.format(a, data[a]))
            #print('buff: {}'.format(buff))
            video_path = buff_video
            frame_folder = buff_frame
            voice_path = buff_voice
            frame_folder = os.path.join(frame_folder, (((data[a].split('/'))[-1]).split('.'))[0])
            is_dir(os.path.join(ROOT, frame_folder))
            frame_list.append(frame_folder)
            if (data[a].split('.'))[-1] ==  'webm':
                voice_path = os.path.join(voice_path, ((data[a].split('/'))[-1]).replace('.webm', '.mp3'))
                voice_list.append(voice_path)
                rename = (((data[a].split('/'))[-1]).split('.'))[0]
                rename+='.mp4'
                video_path = os.path.join(video_path, rename)
                path_list.append(video_path)
                #webm to mp4
                webm_to_mp4(data[a], os.path.join(ROOT, video_path))
                make_frames(os.path.join(ROOT, video_path), os.path.join(ROOT, frame_folder))
                extract_voice(os.path.join(ROOT, video_path), os.path.join(ROOT, voice_path))
                continue
            video_path = os.path.join(video_path, (data[a].split('/'))[-1])
            voice_path = os.path.join(voice_path, ((data[a].split('/'))[-1]).replace('.mp4', '.mp3'))
            voice_list.append(voice_path)
            #print('voice_path  : '+voice_path)
            #print('video_path  : '+video_path)
            #exit()
            shutil.copy(video_path.replace('videos/', ''), video_path)
            make_frames(os.path.join(ROOT, video_path), os.path.join(ROOT, frame_folder))
            extract_voice(os.path.join(ROOT, video_path), os.path.join(ROOT, voice_path))
            path_list.append(video_path)
    path_list.sort()
    frame_list.sort()
    voice_list.sort()
    file_frame = open('frames_path_{}.txt'.format(type), 'w')
    file_video = open('videos_path_{}.txt'.format(type), 'w')
    file_voice = open('voices_path_{}.txt'.format(type), 'w')
    for path in path_list: #データパスの書き込み
        file_video.write(path+'\n')
    file_video.close()
    for path in frame_list: #データパスの書き込み
        file_frame.write(path+'\n')
    file_frame.close()
    for path in voice_list: #データパスの書き込み
        file_voice.write(path+'\n')
    file_voice.close()

    print('----- FINISH -----')

def main():
    types = ['ita', 'tweet']
    for type in types:
        make_dataPath(type)
main()
