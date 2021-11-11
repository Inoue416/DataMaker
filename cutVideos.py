import os
import cv2

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
        os.system(self.c_cmd.format(second, vp, second+self.cut_num, os.path.join(save_path, ("{}To{}"+ext).format(second, second+self.cut_num))))
        CutVideos.make_path(save_path, ((vp.split("/"))[-1]).replace(ext, '.txt'), ("{}To{}"+ext).format(second, second+self.cut_num))
        second += self.cut_num
        self._run_cmd(second, max_second, vp, save_path, ext)

    # 処理開始の関数
    def _cut_videos(self):
        CutVideos.exists_folder(self.svp)
        print("-"*10, " START CUTTING ","-"*10)
        if self.vps == None:
            return False
        for vp in self.vps:
            vp = CutVideos.to_mp4(vp)
            cap = cv2.VideoCapture(vp)
            if not cap.isOpened():
                print("{} isn't exists.".format(vp))
                cap.release()
                continue
            video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
            cap.release()
            save_folder, ext = os.path.splitext((vp.split('/'))[-1])
            save_path = os.path.join(self.svp, save_folder)
            CutVideos.exists_folder(save_path)
            self._run_cmd(0, video_length, vp, save_path, ext)
        print("-"*10, " FINSH CUTTING ","-"*10)
        return True


    # フォルダがあればスキップ、なければ作成
    @staticmethod
    def exists_folder(path):
        if not os.path.isdir(path):
            os.mkdir(path)

    # 動画をmp4へ変換
    @staticmethod
    def to_mp4(path):
        mp4_cmd = "ffmpeg -i {} {}.mp4"
        save_name, ext = os.path.splitext((path.split('/'))[-1])
        if ext == ".mp4":
            return path
        os.system(mp4_cmd.format(path, os.path.join(path.replace(save_name+ext, ''),save_name)))
        return os.path.join(path.replace(save_name+ext, ''),save_name) + ".mp4"

    # カッティングしたビデオまでのパスの作成
    @staticmethod
    def make_path(save_path, filename, save_name):
        try:
            with open(os.path.join(save_path, filename), 'a') as f:
                f.write(os.path.join(save_path, save_name)+'\n')
        except:
            with open(os.path.join(save_path, filename), 'w') as f:
                f.write(os.path.join(save_path, save_name)+'\n')
