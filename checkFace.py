from cutVideos import *
import os
import face_recognition

class CheckFace(CutVideos):
    def __init__(self, vps=None, pp="datas/face_logs"):
        super().__init__(vps=vps, pp=pp)


    def _check_face(self):
        print("-"*10, " START CHECK FACE ", "-"*10)
        j = True
        if self.vps == None:
            print("Not found frame data.")
            print("-"*10, "FAILED", "-"*10, '\n')
            return
        for vp in self.vps:
            print("\nData: ", vp, "\n")
            datas = [os.path.join(vp, filename) for filename in os.listdir(vp)]
            for data in datas:
                image = face_recognition.load_image_file(data)
                face_location = face_recognition.face_locations(image)
                if len(face_location) != 1:
                    j = False
                    break
            if j:
                self.make_path(vp, "success.txt", '')
                # make_path
            else:
                self.make_path(vp, "fail.txt", '')

        print("-"*10, " FINISH CHECK FACE ", "-"*10)
