from cutVideos import *
from makeFrames import MakeFrames
from extractVoice import ExtractVoice
#from checkFace import CheckFace
from extractLips import ExtractLips
from voiceRecognizer import VoiceRecognizer
import os
import sys
import options as opt
import shutil

# TODO: 既存で処理されているデータのスキップと削除

""" TODO:
    フルオートと各フェーズを分ける理由としては、各フェーズがあった方が便利と思うから。
"""


if __name__ == "__main__":
    opt = __import__('options')
    CutVideos.exists_folder(opt.data_root)

def c_v(path, dsv, key):
    # define instance
    print(path, dsv)
    cvs = CutVideos(vps=path, svp=dsv)
    if not cvs._cut_videos():
        print('Not found data.\n')
    return key+1

def mf_and_ev(paths, dsv, key):
    data_paths = []
    for path in paths:
        data_paths.append(os.path.join(opt.fa_data_save[key-1], path))
        # make frames
    mf = MakeFrames(vps=data_paths, svp=dsv[key-1])
    if not mf._making_frames():
        print('Not found data.\n')
    # extract voice
    ev = ExtractVoice(vps=data_paths, svp=dsv[key])
    if not ev._extract_voice():
        print('Not found data.\n')
    return key+1


# face recognize
"""def c_f(datas, ps, key):
    paths = []
    for path in os.listdir(datas):
        paths.extend(load_path(os.path.join(datas, path)))
    cf = CheckFace(vps=paths, pp=ps)
    cf._check_face()
    return key+1"""

# extract lips from frames.
def e_l(datas, dsv, key, kind_no):
    frames_data = [os.path.join(datas, fname) for fname in kind_no]
    frames_data.sort()
    el = ExtractLips(vps=frames_data, svp=dsv)
    el._extract_lips()
    return key+1


def v_r(datas, dsv, key, kind_no):
    data_paths = [os.path.join(datas, fname) for fname in kind_no]
    data_paths.sort()
    vr = VoiceRecognizer(vps=data_paths, svp=dsv, pre_weight=opt.vr_preweight)
    vr._voice_recognition()
    return

def get_media_path():
    copy_path = 'datas/originDatas'
    path = os.path.join(opt.media_path, opt.media_name)
    if not os.path.isdir(os.path.join(opt.media_path, opt.media_name)):
        print(os.path.join(opt.media_path, opt.media_name))
        print("This path don't exists.")
        print("Check media options.")
        exit()
    folders = os.listdir(path)
    folders.sort()
    index = []
    i = 0
    for folder in folders:
        if 'System' in folder:
            index.append(i)
        i+=1
    if index != []:
        for idx in index:
            folders.pop(idx)
    paths = [os.path.join(path, folder) for folder in folders]
    return paths

def setup_data(data_folder, total_data_num):
    print("target folder: ")
    print(data_folder)
    datas = os.listdir(data_folder)
    datas.sort()
    result_total = total_data_num
    kind_no = []
    for cn in range(len(datas)):
        print(datas[cn])
        _, ext = os.path.splitext(datas[cn])
        filename = 'no_{}{}'.format(result_total, ext)
        kind_no.append('no_{}'.format(result_total))
        print(filename)
        #shutil.copy2(os.path.join(data_folder, datas[cn]), os.path.join(opt.full_auto_path, filename))
        result_total += 1
    return result_total, kind_no


# Full auto mode
def full_auto(paths, kind_no):
    count = 2 #0
    #count = c_v(paths, opt.fa_data_save[count], count)
    #paths = os.listdir(opt.fa_data_save[count-1])
    #count = mf_and_ev(paths, opt.fa_data_save[count], count)
    count = e_l(opt.fa_data_save[count-1][0], opt.fa_data_save[count], count, kind_no)
    count = v_r(opt.fa_data_save[count-2][1], opt.fa_data_save[count], count, kind_no)
    return

# Manual mode
"""def manual(choose, filename):
    # データのパスのロード
    if choose == "0":
        if not self.exists_file(os.path.join(opt.data_origin, filename)):
            print(filename, " isn't.\n")
        c_v([os.path.join(opt.data_origin, filename)], opt.data_save[0], opt.s_path[0], 0)

    elif choose == "1":
        if not self.exists_file(os.path.join(opt.d_path[0], filename)):
            print(filename, " isn't.\n")
        m_f_and_ev([filename], opt.data_save[1], opt.s_path[1],1)

    elif choose == "2":
        if not self.exists_file(os.path.join(opt.d_path[1], filename)):
            print(filename, " isn't.\n")
        datas = load_path(os.path.join(opt.d_path[1], filename))
        c_f(datas, opt.s_path[2], 0)

    elif choose == "3":
        if not self.exists_file(os.path.join(opt.d_path[1], filename)):
            print(filename, " isn't.\n")
        datas = load_path(os.path.join(opt.d_path[1], filename))
        e_l(datas, )

    elif choose == "4":
        v_r()

    return"""

if __name__ == "__main__":
    total_data_num = 91
    data_folders = get_media_path()
    print(data_folders)

    for i in range(2, len(data_folders)):#opt.copy_folder_num):
        print("-"*10, ' DATA LOAD ', "-"*10, '\n')
        total_data_num, kind_no = setup_data(data_folders[i], total_data_num)
        print(total_data_num)
        print(kind_no)
        #exit()
        print("-"*10, ' COMPLETE ', "-"*10, '\n')

        print("-"*10, ' DATA LOAD ', "-"*10, '\n')
        path= opt.full_auto_path
        path = [os.path.join(path, f) for f in os.listdir(path)]
        #if not path:
            #print("No file.")
            #exit()
        print("-"*10, ' COMPLETE ', "-"*10, '\n')
        full_auto(path, kind_no)
    """judge = True
    while judge:
        print("Choose phase.")
            #0: making short videos.
            #1: making frames of 0 and extract voice of 0.
            #2: check face in frames. if not find face, write log file.
            #3: extract lips from frames of 1.
            #4: voice data to text data.
            #5: full auto.
        while True:
            print("0: Cut videos\n1: Make frames and Extract voice\n2: Check faces\n3: Extract lips\n4: Voice recognize\n5: Full auto")
            choose = input("\nINPUT: ")
            print()
            if choose == "0" or choose == "1" or choose == "2" or choose == "3" or choose=="4" or choose=="5":
                break
            print("\nInput error.")
            print("Please input 0 or 1 or 2 or 3 or 4 or 5 only.\n")

    # データのロード
        if choose != "5":
            print("-"*10, ' LOAD DATA PATH ', "-"*10, '\n')
            print("Input name of load file.")
            filename = input("INPUT: ")
            manual(choose, filename)
            
        else:
            print("-"*10, ' AUTO LOAD ', "-"*10, '\n')
            path= opt.full_auto_path
            path = [os.path.join(path, f) for f in os.listdir(path)]
            if not path:
                print("No file.")
                break
            full_auto(path)

        while True:
            print("\n0: FINISH  1: CONTINUE")
            j = input("INPUT: ")
            if j == "0":
                judge = False
                break
            elif j == "1":
                break
            else:
                print("\nInput error.")
                print("Please input 0 or 1 only.")"""
    print("\n", "-"*10 ," END ", "-"*10)
