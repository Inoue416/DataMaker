import os
from cutVideos import CutVideos
import cv2


class ExtractVoice(CutVideos):
    def __init__(self, vps=None, svp="datas/voice", pp="datas/voice_path", c_cmd="ffmpeg -i {} -f mp3 {}.mp3"):
        super().__init__(vps, svp, pp, c_cmd)

    def _run_cmd(self, vp, save_path):
        filename = ((vp).split('/'))[-1]
        filename, _ = os.path.splitext(filename)
        #print(os.path.join(save_path, filename+'.mp3'))
        #exit()
        if self.exists_file(os.path.join(save_path, filename+'.mp3')):
            return
        os.system(self.c_cmd.format(vp, os.path.join(save_path, filename)))
        self.make_path(save_path, (((vp).split('/'))[-2])+".txt", filename+'.mp3')

    def _extract_voice(self):
        self.exists_folder(self.svp)
        print("-"*10, " START EXTRACT VOICE ","-"*10)
        if self.vps == None:
            return False
        for vp in self.vps:
            #self.list_results(vp)
            cap = cv2.VideoCapture(vp)
            if not cap.isOpened():
                print("\n{} isn't exists.\n".format(vp))
                cap.release()
                continue
            cap.release()
            save_folder, _ = os.path.splitext((vp.split('/'))[-1])
            save_path = os.path.join(self.svp, (vp.split('/'))[-2])
            self.exists_folder(save_path)
            self._run_cmd(vp, save_path)
        print("-"*10, " FINSH EXTRACT VOICE ","-"*10)
        return True
