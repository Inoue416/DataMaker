from cutVideos import *
from makeFrames import MakeFrames
from extractVoice import ExtractVoice
from checkFace import CheckFace
from extractLips import ExtractLips
from voiceRecognizer import VoiceRecognizer
import os
import sys
import options as opt



""" TODO:
    フルオートと各フェーズを分ける理由としては、各フェーズがあった方が便利と思うから。
"""


if __name__ == "__main__":
    opt = __import__('options')
    CutVideos.exists_folder(opt.data_root)

def load_path(path):
    paths = []
    print("\nLoad data path now ...")
    try:
        with open(path, 'r') as f:
            r = ((f.read()).split('\n'))
            r.remove('')
            paths.extend(r)
            print("Complete.\n")
        return paths
    except:
        print("Failed.\n")
        return None

def c_v(path, dsv, sv, key):
    # define instance
    cvs = CutVideos(vps=path, svp=dsv, pp=sv)
    if not cvs._cut_videos():
        print('Not found data.\n')
    return key+1

def m_f_and_ev(paths, dsv, ps, key):
    data_paths = []
    for path in paths:
        data_paths.append(os.path.join(opt.fa_d_path[key-1], path))
        # make frames
    paths = []
    for data_path in data_paths:
        paths.extend(load_path(data_path))
    mf = MakeFrames(vps=paths, svp=dsv[key-1], pp=ps[key-1])
    if not mf._making_frames():
        print('Not found data.\n')
    # extract voice
    ev = ExtractVoice(vps=paths, svp=dsv[key], pp=ps[key])
    if not ev._extract_voice():
        print('Not found data.\n')
    return key+1


# face recognize
def c_f(datas, ps, key):
    paths = []
    for path in os.listdir(datas):
        paths.extend(load_path(os.path.join(datas, path)))
    cf = CheckFace(vps=paths, pp=ps)
    cf._check_face()
    return key+1

# extract lips from frames.
def e_l(datas, dsv, ps, key):
    datas = load_path(datas)
    el = ExtractLips(vps=datas, svp=dsv, pp=ps)
    el._extract_lips()
    return key+1


def v_r(datas, dsv, key):
    paths = []
    for path in os.listdir(datas):
        paths.extend(load_path(os.path.join(datas, path)))
    vr = VoiceRecognizer(vps=paths, svp=dsv, pre_weight=opt.vr_preweight)
    vr._voice_recognition()
    return


# Full auto mode
def full_auto(paths):
    count = 0
    count = c_v(paths, opt.fa_data_save[count], opt.fa_s_path[count], count)
    paths = os.listdir(opt.fa_d_path[count-1])
    count = m_f_and_ev(paths, opt.fa_data_save[count], opt.fa_s_path[count], count)
    count = c_f(opt.fa_d_path[count-1], opt.fa_s_path[count], count)
    count = e_l(opt.fa_d_path[count-1], opt.fa_data_save[count-1], opt.fa_s_path[count], count)
    count = v_r(opt.fa_d_path[count-1], opt.fa_data_save[count-1], count)
    return

# Manual mode
def manual():
    return

if __name__ == "__main__":
    judge = True
    while judge:
        print("Choose phase.")
        """
            0: making short videos.
            1: making frames of 0 and extract voice of 0.
            2: check face in frames. if not find face, write log file.
            3: extract lips from frames of 1.
            4: voice data to text data.
            5: full auto.
        """
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
            path = os.path.join(opt.data_root, filename)
            path = load_path(path)
        else:
            print("-"*10, ' AUTO LOAD ', "-"*10, '\n')
            path= opt.full_auto_path
            path = [os.path.join(path, f) for f in os.listdir(path)]
            if not path:
                print("No file.")
                break
            full_auto(path)
        # データのパスのロード
        """if choose == "0":
            c_v(path, choose)
        elif choose == "1":
            m_f_and_ev(path, choose)
        elif choose == "2":
            c_f()
        elif choose == "3":
            v_r()
        elif choose == "4":
            e_l()"""

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
                print("Please input 0 or 1 only.")
    print("\n", "-"*10 ," END ", "-"*10)
