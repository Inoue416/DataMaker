import os
from cutVideos import CutVideos
import cv2


class MakeFrames(CutVideos):
    def __init__(self, vps=None, svp="datas/frames", pp="datas/frames_path", c_cmd="ffmpeg -i {} -r {} {}/%03d.jpg", cut_num=0):
        super().__init__(vps, svp, pp, c_cmd, cut_num)

    def _run_cmd(self, vp, save_path):
        os.system(self.c_cmd.format(vp, self.cut_num, save_path))
        self.make_path(save_path, (save_path.split('/')[-2])+'.txt', '')

    def _making_frames(self):
        self.exists_folder(self.svp)
        print("-"*10, " START MAKING FRAMES ","-"*10)
        if self.vps == None:
            print("\nNot found video data.\n")
            print("-"*10, "FAILED", "-"*10, '\n')
            return False
        for vp in self.vps:
            #self.list_results(vp)
            print("\nData: ", vp, "\n")
            cap = cv2.VideoCapture(vp)
            if not cap.isOpened():
                print("\n{} isn't exists.\n".format(vp))
                cap.release()
                continue
            self.cut_num = int(cap.get(cv2.CAP_PROP_FPS))
            cap.release()
            save_folder, _ = os.path.splitext((vp.split('/'))[-1])
            save_path = os.path.join(self.svp, (vp.split('/'))[-2])
            self.exists_folder(save_path)
            save_path = os.path.join(save_path, save_folder)
            self.exists_folder(save_path)
            if os.listdir(save_path) != []:
                print('\nExists frames.\n')
                continue
            print("Make frames now ...")
            self._run_cmd(vp, save_path)
        print("-"*10, " FINSH MAKING FRAMES ","-"*10)
        return True
