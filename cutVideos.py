import os
import cv2
import options as opt
import shutil

class CutVideos():
    def __init__(self, vps=None, svp="datas/cut_videos", c_cmd="ffmpeg -ss {} -i {} -to {} -c copy {}", cut_num=3): # video path, save path
        self.vps = vps
        self.svp = svp
        self.c_cmd = c_cmd
        self.cut_num = cut_num


    # ビデオのカッティング処理
    def _run_cmd(self, second, max_second, vp, save_path, ext):
        if (second+self.cut_num) > max_second:
            return
        if not self.exists_file(os.path.join(save_path, ("{}To{}"+ext).format(second, second+self.cut_num))):
            os.system(self.c_cmd.format(second, vp, second+self.cut_num, os.path.join(save_path, ("{}To{}"+ext).format(second, second+self.cut_num))))
            #self.make_path(save_path, ((vp.split("/"))[-1]).replace(ext, '.txt'), ("{}To{}"+ext).format(second, second+self.cut_num))
        second += self.cut_num
        self._run_cmd(second, max_second, vp, save_path, ext)

    # 処理開始の関数
    def _cut_videos(self):
        self.exists_folder(self.svp)
        print("-"*10, " START CUTTING ","-"*10)
        if self.vps == None:
            print("Not found video data.")
            print("-"*10, "FAILED", "-"*10, '\n')
            return False
        for vp in self.vps:
            print("\nData: ", vp, "\n")
            #self.list_results(vp)
            vp = self.to_mp4(vp)
            cap = cv2.VideoCapture(vp)
            if not cap.isOpened():
                print("{} isn't exists.".format(vp))
                cap.release()
                continue
            ll= int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            #print(ll)
            if (ll == 19):
                ll = 14*30
            video_length = (ll / cap.get(cv2.CAP_PROP_FPS))
            #video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
            cap.release()
            #exit()
            save_folder, ext = os.path.splitext((vp.split('/'))[-1])
            save_path = os.path.join(self.svp, save_folder)
            #print(save_path)
            #exit()
            CutVideos.exists_folder(save_path)
            print("Cutting now ...")
            self._run_cmd(0, video_length, vp, save_path, ext)
        print("-"*10, " FINSH CUTTING ","-"*10)
        _, _, free = shutil.disk_usage('/')
        free = int(free/(10**9))
        if (free <= 3):
            print('Must increase capacity.')
            exit()
        return True

    # 処理結果をひとまとめにする作業
    """def list_results(self, vp):
        if bool(self.rlfn):
            save_folder, ext = os.path.splitext((vp.split('/'))[-1])
            self.make_path(self.pp, self.rlfn, ((vp.split('/'))[-1]).replace(ext, '.txt'))
        else:
            print("\nNot set file of results listing.\n")"""

    # フォルダがあればスキップ、なければ作成
    @staticmethod
    def exists_folder(path):
        if os.path.isdir(path):
            return
        os.mkdir(path)

    # 動画をmp4へ変換
    def to_mp4(self, path):
        mp4_cmd = "ffmpeg -i {} {}.mp4"
        save_name, ext = os.path.splitext((path.split('/'))[-1])
        if ext == ".mp4":
            return path
        if not self.exists_file(path.replace(ext, '.mp4')):
            try:
                print(ext, ' to mp4 ...')
                os.system(mp4_cmd.format(path, os.path.join(path.replace(save_name+ext, ''),save_name)))
            except:
                print("Not change this file.")
                exit()
        return os.path.join(path.replace(save_name+ext, ''),save_name) + ".mp4"

    def exists_file(self, path):
        if os.path.isfile(path):
            print('\n', path)
            print('This file is already exists.\n')
            return True
        else:
            return False
