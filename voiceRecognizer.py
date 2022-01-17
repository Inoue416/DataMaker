import os
import soundfile
from cutVideos import *
from espnet2.bin.asr_inference import Speech2Text
from espnet_model_zoo.downloader import ModelDownloader
import shutil

class VoiceRecognizer(CutVideos):
    def __init__(self, vps=None, svp="datas/anno_data", pre_weight=None):
        super().__init__(vps, svp)
        self.pre_weight = pre_weight

    def _write_anno(self, text, foldername, filename):
        try:
            with open(os.path.join(self.svp, foldername, filename+".txt"), 'w') as f:
                print('Results: ', text)
                print("Writting now ...")
                f.write(text)
        except:
            print("Not found {}\n".format(os.path.join(self.svp, foldername)))
            print("Can't write result.\n")

    def _voice_recognition(self):
        print("-"*10, " START SPEECH TO TEXT ", "-"*10)

        self.exists_folder(self.svp)
        if not self.pre_weight:
            print("\nCan't load weights.\n")
            print("-"*10, "FAILED", "-"*10, '\n')
            return
        if self.vps == None:
            print("\nNot found voice data.\n")
            print("-"*10, "FAILED", "-"*10, '\n')
            return
        #self.exists_folder(self.svp)
        d = ModelDownloader()
        d.download_and_unpack(self.pre_weight)
        speech2text = Speech2Text.from_pretrained(
            self.pre_weight,
            maxlenratio=0.0,
            minlenratio=0.0,
            beam_size=20,
            ctc_weight=0.3,
            lm_weight=0.5,
            penalty=0.0,
            nbest=1
        )
        for vp in self.vps:
            print("\nData: ", vp, "\n")
            data_paths = [os.path.join(vp, file) for file in os.listdir(vp)]
            if data_paths == []:
                continue
            data_paths.sort()
            for data in data_paths:
                print("\nData: ", data, "\n")
                filename = data.split('/')
                foldername = filename[-2]
                filename = filename[-1]
                filename, _ = os.path.splitext(filename)
                speech, rate = soundfile.read(data)
                nbests = speech2text(speech)
                text, *_ = nbests[0]
                print(text)
                print(filename)
                #exit()
                self.exists_folder(os.path.join(self.svp, foldername))
                if not self.exists_file(os.path.join(self.svp, foldername, filename+'.txt')):
                    self._write_anno(text, foldername, filename)
        print("-"*10, " FINISH SPEECH TO TEXT ", "-"*10)
        _, _, free = shutil.disk_usage('/')
        free = int((free/(10**9)))
        if (free <= 3):
            print('Must increase capacity.')
            exit()

