import os
from cutVideos import CutVideos
import cv2
import shutil

"""
    c_cmd = "ffmpeg -i {} -f wav -ar 16000 {}.wav" 音声認識を用いるときはこれの方が良いかもしれない
    一般的な音声認識では量子化ビット数16ビット、サンプリング周波数16kHzで用いるから。
"""
class ExtractVoice(CutVideos):
    def __init__(self, vps=None, svp="datas/voice", c_cmd="ffmpeg -i {} -f wav -ar 16000 {}.wav"):
        super().__init__(vps, svp, c_cmd)

    def _run_cmd(self, vp, save_path):
        filename = ((vp).split('/'))[-1]
        filename, _ = os.path.splitext(filename)
        #print(os.path.join(save_path, filename+'.mp3'))
        #exit()
        if self.exists_file(os.path.join(save_path, filename+'.wav')):
            return
        os.system(self.c_cmd.format(vp, os.path.join(save_path, filename)))
        #self.make_path(save_path, (((vp).split('/'))[-2])+".txt", filename+'.wav')

    def _extract_voice(self):
        self.exists_folder(self.svp)
        print("-"*10, " START EXTRACT VOICE ","-"*10)
        if self.vps == None:
            print("\nNot found video data.\n")
            print("-"*10, "FAILED", "-"*10, '\n')
            return False
        for vp in self.vps:
            print("\nData: ", vp, "\n")
            #self.list_results(vp)
            
            data_paths = [os.path.join(vp, file) for file in os.listdir(vp)]
            if data_paths == []:
                continue
            data_paths.sort()
            #print(data_paths)
            for data in data_paths:
                print("\nData: ", data, "\n")
                cap = cv2.VideoCapture(data)
                if not cap.isOpened():
                    print("\n{} isn't exists.\n".format(data))
                    cap.release()
                    continue
                cap.release()
                save_folder, _ = os.path.splitext((data.split('/'))[-1])
                save_path = os.path.join(self.svp, (data.split('/'))[-2])
                self.exists_folder(save_path)
                self._run_cmd(data, save_path)
        print("-"*10, " FINSH EXTRACT VOICE ","-"*10)
        _, _, free = shutil.disk_usage('/')
        free = int((free/(10**9)))
        if (free <= 3):
            print('Must increase capacity.')
            exit()
        return True
